from typing import TypeVar, Generic, Callable

T = TypeVar('T') # generic type

# TODO: Find best hashing function
# TODO: Add uniformity testing for hashing function i.e. Pearson's Chi Squared function
# TODO: Add load factor calculation
# TODO: Handle table resizing

class HashTable:
    def __init__(self):
        self.table_size: int = 100
        self.table: List[T] = [None] * self.table_size
        self.filled_count: int = 0
        self.hash_fn = self.toy_hash # setup hashing function to use

    def __len__(self) -> int:
        """ Returns number of (key, value) pairs in table """
        return self.filled_count
    
    def __repr__(self) -> str:
        """ Returns a string representation of the hash table à la Python's dict's {key1: value1, key2: value2} """
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
        # TODO

    @staticmethod
    def toy_hash(key: T, table_size: int) -> int:
        """ Hashing function """
        int_equiv: int = hash(key) # get an int representation of T

        # TODO: Your hash function customization goes here
        idx: int = (int_equiv * 53) % table_size # toy "hashing function"
        return idx

    @staticmethod
    def uniformity_test(self, fn: Callable) -> float:
        """ Uniformity test for hash fn using Pearson's Chi squared function """
        # TODO

    def probe(self, start: int) -> int:
        """ For Open Addressing, probe linearly for next free position from start """
        count: int = 0
        for i in range(self.table_size):
            idx = (start + i) % self.table_size
            if self.table[idx] is None: # found a free spot
                return idx
            count += 1
            if count == self.table_size:
                # hash table completely filled
                # TODO: resize table
                raise NotImplementedError("Table filled")
    
    def update(self, key: T, value: T) -> None:
        """ Handles inserts and updates of (key, value) pairs to hash table """
        idx: int = self.hash_fn(key, self.table_size) # get an index location for 'key'
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
        idx: int = self.hash_fn(key, self.table_size) # get an index location for 'key'
        if self.table[idx] is None: # 'key' doesn't exists in hash table
            raise Exception("Key doesn't exist in hashtable")
        else:
            return self.table[idx][1] # return pair value
    
    def delete(self, key: T) -> None:
        """ Deletes a (key, value) pair from the hash table """
        idx: int = self.hash_fn(key, self.table_size) # get an index location for 'key'
        if self.table[idx] is None: # 'key' doesn't exists in hash table
            raise Exception("Key doesn't exist in hashtable")
        else:
            self.table[idx] = None # delete value at 'key'
            self.filled_count -= 1

if __name__ == "__main__":
    table = HashTable()
    print(table)
    table["asfsadf"] = "334345"
    print(table)
    table["asfsadf"] = 555555
    print(table['asfsadf'])
    print(table)