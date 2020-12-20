from typing import TypeVar, Callable, List
from random import randint

T = TypeVar('T')

class HashTable:
    def __init__(self):
        self.table_size: int = 23
        self.table: List[(T, T)] = [None] * self.table_size
        self.filled_count: int = 0
        self.hash_fn: Callable = self.crc32_hash # or self.prime_mod_hash
        self.resize_threshold: float = 0.75
        self.a: int = randint(1, 2**32) # for prime mod hash
        self.b: int = randint(1, 2**32) # for secondary hashing function
        self.crc32_table: List[int] = self.crc32_table() # for CRC32 algorithm
        self.key_comparison_counts: int = 0 # stats

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
        """
        Encode key (str or int) as an integer
        Strings of arbitrary length are encoded using a polynomial rolling hash scheme
        """
        
        if isinstance(key, str):
            result: int = 0
            p: int = 97 # p should roughly equal the number of characters in the input alphabet, we have 95 printable ASII chars
            m: int = 32361122672259149 # now that's a prime :), 19th in OEIS A118839
            p_pow: int = 1
            for c in key:
                result = (result + ord(c) * p_pow) % m
                p_pow = (p_pow * p) % m
            return result
        elif isinstance(key, int):
            return key
        else:
            raise Exception(f"Cannot encode {type(key)} (Only strings and integers are supported)")

    def prime_mod_hash(self, key: T) -> int:
        """ Returns a hash of key using h(k) = (a * key) mod m where m is a prime number """
        return (self.a * self.encode(key)) % self.table_size
    
    @staticmethod
    def crc32_table() -> List[int]:
        """ Returns a table of values for use with the CRC32 hash """

        table: List[int] = []
        for i in range(256):
            k: int = i
            for j in range(8):
                if k & 1:
                    k ^= 0x1db710640
                k >>= 1
            table.append(k)
        return table

    def crc32_hash(self, key: T) -> int:
        """ Returns a hash of key using CRC32 """

        if isinstance(key, str):
            crc32: int = 0xffffffff
            for b in key.encode('utf-8'):
                crc32 = (crc32 >> 8) ^ self.crc32_table[(crc32 & 0xff) ^ b]
            crc32 ^= 0xffffffff # invert all bits
            return crc32 % self.table_size
        else:
            return self.prime_mod_hash(key)
    
    def h2(self, key) -> int:
        """ Secondary hashing function for double hashing """
        idx: int = (self.b * self.encode(key)) % self.table_size
        return idx if idx != 0 else 1

    def find(self, key: T) -> int:
        """ Find first occupied position using double hashing """

        try:
            # passes check with primary hashing function
            idx: int = self.hash_fn(key)
            if self.table[idx][0] == key:
                return idx

            # use secondary function to find an interval to use
            # i.e. if they had no matching value, double hashing is used to probe to the next key
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

        idx: int = self.hash_fn(key) # get an index location for 'key'
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

        idx: int = self.hash_fn(key) # get an index location for 'key'
        if self.table[idx] is None: # 'key' doesn't exists in hash table
            raise Exception("Key doesn't exist in hashtable")
        else:
            self.key_comparison_counts += 1
            return self.table[self.find(key)][1] # return pair value
    
    def delete(self, key: T) -> None:
        """ Deletes a (key, value) pair from the hash table """

        idx: int = self.hash_fn(key) # get an index location for 'key'
        if self.table[idx] is None: # 'key' doesn't exists in hash table
            raise Exception("Key doesn't exist in hashtable")
        else:
            self.table[self.find(key)] = None # delete value at 'key'
            self.filled_count -= 1
    
    def resize(self) -> None:
        """
        Increases the table's size once the load factor reaches self.threshold
        The table is resized to the smallest prime number > 2 * the current size
        Primality testing is done using the deterministic variant of Rabin Miller for n < 3,317,044,064,679,887,385,961,981
        """

        size: int = 2 * self.table_size + 1
        while True:
            is_prime: bool = True
            for d in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
                if size % d == 0:
                    size += 2
                    is_prime = False
                    break
            if is_prime:
                break

        # rehash all entries of the hash table after the increase in table size
        temp: List[(T, T)] = self.table
        self.table_size = size
        self.table = [None] * self.table_size
        self.filled_count = 0

        for pair in temp:
            if pair is not None:
                self[pair[0]] = pair[1]
    
def key_comparison_stats(n: int, test_data: List[str]) -> (float, int):
    mmax: int = 0
    total: int = 0
    for _ in range(1024):
        table = HashTable()
        for t in ts[:n]:
            table[t] = 1
        
        for t in ts[:n]:
            table.key_comparison_counts = 0
            table[t]
            mmax = max(table.key_comparison_counts, mmax)
            total += table.key_comparison_counts
    return total / (len(table) * 1024), mmax

if __name__ == "__main__":
    ts: List[str] = ["the", "of", "and", "to", "a", "in", "for", "is", "on", "that", "by", "this", "with", "i", "you", "it", "not", "or", "be", "are", "from", "at", "as", "your", "all", "have", "new", "more", "an", "was", "we", "will", "home", "can", "us", "about", "if", "page", "my", "has", "search", "free", "but", "our", "one", "other", "do", "no", "information", "time"]

    print("Input size of 6")
    t: (float, int) = key_comparison_stats(6, ts)
    print(f"Average is: {t[0]}, Max is: {t[1]}")

    print("\nInput size of 20")
    t: (float, int) = key_comparison_stats(20, ts)
    print(f"Average is: {t[0]}, Max is: {t[1]}")

    print("\nInput size of 50")
    t: (float, int) = key_comparison_stats(50, ts)
    print(f"Average is: {t[0]}, Max is: {t[1]}")