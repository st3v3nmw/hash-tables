from hashtable import HashTable
import json
import matplotlib.pyplot as plt
from typing import List

def uniformity_test(table_size: int) -> float:
    """
    Uniformity test for hash fn using Pearson's Chi squared test
    The returned value should be within 0.95 <= r <= 1.05 for a good hash function
    """

    table = HashTable()
    table.table_size = table_size
    buckets: List[int] = [0] * table_size

    with open("test data/google-10000-english-no-swears.txt", "r") as f:
        test_data: List[str] = json.load(f)
    
    n_observations: int = len(test_data)
    for x in test_data:
        buckets[table.hash_fn(x)] += 1
    
    tt = 0
    for b in buckets:
        tt += b * (b + 1) / 2
    return tt / (n_observations / (2 * table_size) * (n_observations + 2 * table_size - 1))

if __name__ == "__main__":
    # test uniformity for prime_mod_hash function for various table sizes s
    xs: List[int] = []
    ys: List[int] = []
    for s in range(2, 256):
        xs.append(s)
        ys.append(uniformity_test(s))
    print(f"Average is: {sum(ys) / len(ys)}, Max is: {max(ys)}")
    plt.title("Uniformity Test")
    plt.plot(xs, ys)
    plt.xticks([i for i in range(0, 261, 10)])
    plt.ylim([0,10])
    plt.yticks([i for i in range(10)])
    plt.grid()
    plt.show()