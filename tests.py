import unittest
from hashtable import HashTable
from random import randint, random
import binascii

class TestHashTableMethods(unittest.TestCase):
    def test_empty_table(self):
        table = HashTable()
        self.assertEqual(str(table), '{}')
        self.assertEqual(len(table), 0)
        self.assertEqual(table.load_factor, 0)
    
    def test_update_ops(self):
        table = HashTable()
        table['answer'] = 42                    # or table.update('answer', 42)
        self.assertEqual(table['answer'], 42)   # or self.assertEqual(table.lookup('answer', 42))
        table[53] = "test"
        table[53] = "updated"
        self.assertEqual(table[53], "updated")
        self.assertEqual(len(table), 2)
        self.assertAlmostEqual(table.load_factor, 2 / table.table_size)

    def test_delete(self):
        table = HashTable()
        table['answer'] = 42
        table[53] = 1.618
        del table[53]                           # or table.delete(53)
        with self.assertRaises(Exception):
            table[53]
        self.assertAlmostEqual(table.load_factor, 1 / table.table_size)
    
    def test_encoding(self):
        with self.assertRaises(Exception):
            HashTable.encode(1.555)
        self.assertEqual(HashTable.encode("Azc8{"), 10941154641)
        
    def test_en_masse(self):
        table = HashTable()
        test_data = {randint(1, 1024): random() for _ in range(512)}
        for key in test_data:
            table[key] = test_data[key]

        for key in test_data:
            self.assertEqual(table[key], test_data[key])

    def test_crc32(self):
        table = HashTable()
        table.hash_fn = table.crc32_hash
        self.assertEqual(table.crc32_hash("C'est la vie"), 0x2805c0d0 % table.table_size)
        self.assertEqual(table.crc32_hash("hello-world"), binascii.crc32(b"hello-world") % table.table_size)

if __name__ == "__main__":
    unittest.main()