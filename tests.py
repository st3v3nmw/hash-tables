import unittest
from hashtable import HashTable

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
        self.assertAlmostEqual(table.load_factor, 0.06451613)

    def test_delete(self):
        table = HashTable()
        table['answer'] = 42
        table[53] = 1.618
        del table[53]                           # or table.delete(53)
        with self.assertRaises(Exception):
            table[53]
        self.assertAlmostEqual(table.load_factor, 0.03225806)
    
    def encoding(self):
        with self.assertRaises(Exception):
            HashTable.encode('q' * 20)
        with self.assertRaises(Exception):
            HashTable.encode(1.555)
        with self.assertRaises(Exception):
            HashTable.encode(2**32 + 2)

if __name__ == "__main__":
    unittest.main()