from hashtable import HashTable
from typing import Callable
from random import randint
import json

def uniformity_test(fn: Callable, table_size: int = -1) -> float:
    """
    Uniformity test for hash fn using Pearson's Chi squared test
    Returns a p-value in range 0.0 < p <= 1.0 (higher is better?)
    """

    table_size = HashTable.initial_size if table_size == -1 else table_size
    r: int = randint(1, 2**32)
    a: int = r if r % 2 == 1 else r + 1
    buckets: List[int] = [0] * table_size

    with open("test data/google-10000-english-no-swears.txt", "r") as f:
        test_data: List[str] = json.load(f)
    
    n_observations: int = len(test_data)
    t = HashTable.crc32_table()
    for x in test_data:
        if fn == HashTable.prime_mod_hash:
            buckets[fn(x, table_size, a)] += 1
        else:
            buckets[fn(x, table_size, t)] += 1
    
    tt = 0
    for b in buckets:
        tt += b * (b + 1) / 2
    # print(n_observations / table_size, buckets)
    return tt / (n_observations / (2 * table_size) * (n_observations + 2 * table_size - 1))

if __name__ == "__main__":
    # test uniformity for prime_mod_hash function for various table sizes s
    # print(uniformity_test(HashTable.prime_mod_hash, 7))
    # for s in range(2, 256):
    #     p = uniformity_test(HashTable.crc32_hash, s)
    #     print(f"{s}: {p}")


    ts = ["the", "of", "and", "to", "a", "in", "for", "is", "on", "that", "by", "this", "with", "i", "you", "it", "not", "or", "be", "are", "from", "at", "as", "your", "all", "have", "new", "more", "an", "was", "we", "will", "home", "can", "us", "about", "if", "page", "my", "has", "search", "free", "but", "our", "one", "other", "do", "no", "information", "time", "they", "site", "he", "up", "may", "what", "which", "their", "news", "out", "use", "any", "there", "see", "only", "so", "his", "when", "contact", "here", "business", "who", "web", "also", "now", "help", "get", "pm", "view", "online", "c", "e", "first", "am", "been", "would", "how", "were", "me", "s", "services", "some", "these", "click", "its", "like", "service", "x", "than", "find"]

    mmax = 0
    total = 0
    for _ in range(1024):
        # Key comparison counts stats
        table = HashTable()
        for t in ts[:50]:
            table[t] = 1
        
        for t in ts[:50]:
            table.key_comparison_counts = 0
            table[t]
            mmax = max(table.key_comparison_counts, mmax)
            total += table.key_comparison_counts
    
    print(mmax, total / (len(table) * 1024))