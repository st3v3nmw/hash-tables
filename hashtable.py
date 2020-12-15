from typing import TypeVar, Callable
from random import randint
import base64
from math import sqrt

T = TypeVar('T')

# TODO: Make sense of Chi-square test
# TODO: Find alternate(better) hashing function

class HashTable:
    initial_size: int = 23

    def __init__(self, hash_function: Callable = None):
        self.table_size: int = self.initial_size
        self.table: List[(T, T)] = [None] * self.table_size
        self.filled_count: int = 0
        self.hash_fn: Callable = self.prime_mod_hash if hash_function is None else hash_function
        self.resize_threshold: float = 0.75

        # for prime mod hash
        self.a: int = randint(1, 2**32)
        self.b: int = randint(1, 2**32)

        # stats
        self.key_comparison_counts: int = 0

    def __len__(self) -> int:
        """ Returns number of (key, value) pairs in table """
        return self.filled_count
    
    def __repr__(self) -> str:
        """ Returns HashTable's string representation (à la Python's dict's {key1: value1, key2: value2, ..., keyN: valueN}) """

        r: str = "{" + ''.join([ (f'\"{pair[0]}\"' if isinstance(pair[0], str) else str(pair[0])) + ': ' + 
                                 (f'\"{pair[1]}\"' if isinstance(pair[1], str) else str(pair[1])) + ', '
                                 for pair in self.table if pair is not None ])
        return r[:-2] + "}" if len(r) > 1 else "{}"
    
    def __setitem__(self, key: T, value: T) -> None:
        """ Allows `table[key] = value` instead of `table.update(key, value)` """
        self.update(key, value)
    
    def __getitem__(self, key: T) -> T:
        """ Allows `table[key]` instead of `table.lookup(key)` """
        return self.lookup(key)
    
    def __delitem__(self, key: T) -> None:
        """ Allows `del table[key]` instead of `table.delete(key)` """
        self.delete(key)
    
    @property
    def load_factor(self) -> float:
        """ Calculate table's load factor """
        return self.filled_count / self.table_size
    
    @staticmethod
    def encode(key: T) -> int:
        """ Encode key as an integer (unique? representation) """

        if isinstance(key, str):
            if len(key) > 16:
                raise Exception("Maximum string length is 16")
            return int(base64.b16encode(key.encode('utf-8')), 16) # ascii printable characters only
        elif isinstance(key, int):
            if not -2**32 <= key <= 2 ** 32:
                raise Exception("N should be in range -2**32 <= N <= 2**32")
            if key < 1:
                key = key * -1 + 2 ** 32
            return 168139522478581358417196864848638410367 + key
        else:
            raise Exception(f"Cannot encode {type(key)} (Encoding only handles objects of type str and int)")

    @staticmethod
    def prime_mod_hash(key: T, table_size: int, a: int) -> int:
        """
        h(k) = a*key mod m
        Where m is a prime number (Table size is guaranteed to be a prime number)
        """
        return (a * HashTable.encode(key)) % table_size
    
    def h2(self, key) -> int:
        """ Secondary hashing function for double hashing """
        idx: int = self.hash_fn(key, self.table_size, self.b)
        return idx if idx != 0 else 1

    def find(self, key: T) -> int:
        """ Find first occupied position using double hashing """

        try:
            # passes check with primary hashing function
            idx: int = self.hash_fn(key, self.table_size, self.a)
            if self.table[idx][0] == key:
                return idx

            # use secondary function to find an interval to use
            idx2: int = self.h2(key)
            i: int = 1
            while self.table[(idx + i * idx2) % self.table_size][0] != key:
                i += 1
                self.key_comparison_counts += 1
        except TypeError as err:
            raise Exception("Key doesn't exist in hashtable") from err
        return (idx + i * idx2) % self.table_size
    
    def update(self, key: T, value: T) -> None:
        """ Handles inserts and updates of (key, value) pairs to hash table """

        if self.load_factor >= self.resize_threshold:
            self.resize() # increase table size once threshold is reached

        idx: int = self.hash_fn(key, self.table_size, self.a) # get an index location for 'key'
        if self.table[idx] is None: # idx location not occupied
            self.table[idx] = (key, value)
            self.filled_count += 1
        else: # idx location occupied
            if self.table[idx][0] == key: # trying to insert to the same key
                self.table[idx] = (self.table[idx][0], value) # update 'value' at 'key'
            else:
                # probe for next free position using double hashing
                idx2: int = self.h2(key)
                i: int = 1
                while self.table[(idx + i * idx2) % self.table_size] is not None:
                    i += 1
                self.table[(idx + i * idx2) % self.table_size] = (key, value) # insert at an unoccupied location
                self.filled_count += 1
    
    def lookup(self, key: T) -> T:
        """ Handles lookup/search of key in table. Returns value if key is found """

        idx: int = self.hash_fn(key, self.table_size, self.a) # get an index location for 'key'
        if self.table[idx] is None: # 'key' doesn't exists in hash table
            raise Exception("Key doesn't exist in hashtable")
        else:
            self.key_comparison_counts += 1
            return self.table[self.find(key)][1] # return pair value
    
    def delete(self, key: T) -> None:
        """ Deletes a (key, value) pair from the hash table """

        idx: int = self.hash_fn(key, self.table_size, self.a) # get an index location for 'key'
        if self.table[idx] is None: # 'key' doesn't exists in hash table
            raise Exception("Key doesn't exist in hashtable")
        else:
            self.table[self.find(key)] = None # delete value at 'key'
            self.filled_count -= 1
    
    def resize(self) -> None:
        """
        Increases the table's size once the load factor reaches self.threshold
        The table is resized to the smallest prime number > 2 * the current size
        """

        size: int = 2 * self.table_size + 1
        while True:
            is_prime: bool = True
            for d in range(3, int(sqrt(size)) + 1):
                if size % d == 0: # primality testing by trial division
                    size += 2
                    is_prime = False
                    break
            if is_prime:
                break

        # rehash all entries
        temp: List[(T, T)] = self.table
        self.table_size = size
        self.table = [None] * self.table_size
        self.filled_count = 0

        for pair in temp:
            if pair is not None:
                self[pair[0]] = pair[1]

if __name__ == "__main__":
    pass