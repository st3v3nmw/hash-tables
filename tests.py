import unittest
from hashtable import HashTable

class TestHashTableMethods(unittest.TestCase):
    def test_empty_table(self):
        table = HashTable()
        self.assertEqual(str(table), '{}')
        self.assertEqual(len(table), 0)
    
    def test_update_ops(self):
        table = HashTable()
        table['answer'] = 42                    # or table.update('answer', 42)
        self.assertEqual(table['answer'], 42)   # or self.assertEqual(table.lookup('answer', 42))
        table[53] = "test"
        table[53] = "updated"
        self.assertEqual(table[53], "updated")
        self.assertEqual(len(table), 2)

    def test_delete(self):
        table = HashTable()
        table['answer'] = 42
        table[53] = 1.618
        del table[53]                           # or table.delete(53)
        with self.assertRaises(Exception):
            table[53]

if __name__ == "__main__":
    unittest.main()