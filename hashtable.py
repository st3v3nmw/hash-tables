from typing import TypeVar, Callable
from random import randint
import json
import base64
from scipy.stats import chisquare
from math import sqrt

T = TypeVar('T') # generic type (really, just str and int)

# TODO: Make sense of Chi-square test
# TODO: Find alternate(better) hashing function
# TODO: Fix bug where we insert key at a probed location and try to lookup said key
# TODO: Compare quadratic and linear probling
# TODO: Cuckoo hashing

class HashTable:
    def __init__(self, hash_function: Callable = None):
        self.table_size: int = 23
        self.table: List[T] = [None] * self.table_size
        self.filled_count: int = 0
        self.hash_fn: Callable = self.prime_mod_hash if hash_function is None else hash_function
        self.resize_threshold: float = 0.8

        # for prime mod hash
        self.a = randint(1, 2**32)

    def __len__(self) -> int:
        """ Returns number of (key, value) pairs in table """
        return self.filled_count
    
    def __repr__(self) -> str:
        """ Returns HashTable's string representation (à la Python's dict's {key1: value1, key2: value2, ..., keyN: valueN}) """

        r: str = "{"
        for pair in self.table:
            if pair is not None:
                r += (f'\"{pair[0]}\"' if isinstance(pair[0], str) else str(pair[0])) + ': '
                r += (f'\"{pair[1]}\"' if isinstance(pair[1], str) else str(pair[1])) + ', '
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
        """ Encode key as an integer (unique representation?) """

        if isinstance(key, str):
            if len(key) > 16:
                print(key)
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

    @staticmethod
    def uniformity_test(fn: Callable, table_size: int = 23) -> float:
        """
        Uniformity test for hash fn using Pearson's Chi squared test
        Returns a p-value in range 0.0 < p <= 1.0 (higher is better?)
        """

        a = randint(1, 2**32)
        buckets: List[int] = [0] * table_size

        with open("google-10000-english-no-swears.txt", "r") as f:
            test_data = json.load(f)
        
        n_observations: int = len(test_data)
        for x in test_data:
            if fn == HashTable.prime_mod_hash:
                buckets[fn(x, table_size, a)] += 1
            else:
                buckets[fn(x, table_size)] += 1

        return chisquare(buckets)[1]

    def probe(self, start: int) -> int:
        """ For Open Addressing, probe linearly for next free position from start """

        for i in range(self.table_size):
            idx = (start + i) % self.table_size
            if self.table[idx] is None: # found a free spot
                return idx
    
    def update(self, key: T, value: T) -> None:
        """ Handles inserts and updates of (key, value) pairs to hash table """

        if self.load_factor >= self.resize_threshold:
            self.resize() # increase table size once threshold is reached

        idx: int = self.hash_fn(key, self.table_size, self.a) # get an index location for 'key'
        if self.table[idx] is None: # idx location not occupied
            self.table[idx] = (key, value)
            self.filled_count += 1
        else: # idx location occupied
            if self.table[idx][0] == key: # trying to insert to an existing key
                self.table[idx] = (self.table[idx][0], value) # update 'value' at 'key'
            else:
                idx: int = self.probe(idx) # probe for an unoccupied slot
                self.table[idx] = (key, value)
                self.filled_count += 1
    
    def lookup(self, key: T) -> T:
        """ Handles lookup of key in table. Returns value if key is found """

        idx: int = self.hash_fn(key, self.table_size, self.a) # get an index location for 'key'
        if self.table[idx] is None: # 'key' doesn't exists in hash table
            raise Exception("Key doesn't exist in hashtable")
        else:
            return self.table[idx][1] # return pair value
    
    def delete(self, key: T) -> None:
        """ Deletes a (key, value) pair from the hash table """

        idx: int = self.hash_fn(key, self.table_size, self.a) # get an index location for 'key'
        if self.table[idx] is None: # 'key' doesn't exists in hash table
            raise Exception("Key doesn't exist in hashtable")
        else:
            self.table[idx] = None # delete value at 'key'
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
        
        self.table.extend([None] * (size - self.table_size))
        self.table_size = size

if __name__ == "__main__":
    table = HashTable()
    print(table)
    table["asfsadf"] = "334345"
    print(table)
    table["asfsadf"] = 555555
    print(table['asfsadf'])
    print(table)

    for i in range(100):
        table[i] = i

    for i in range(2, 256):
        p = HashTable.uniformity_test(HashTable.prime_mod_hash, i)
        if p > 0.0001:
            print(f"{i}: {p}")