from hashtable import HashTable
import json

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
    for s in range(2, 256):
        p = uniformity_test(s)
        print(f"{s}: {p}")


    # ts = ["the", "of", "and", "to", "a", "in", "for", "is", "on", "that", "by", "this", "with", "i", "you", "it", "not", "or", "be", "are", "from", "at", "as", "your", "all", "have", "new", "more", "an", "was", "we", "will", "home", "can", "us", "about", "if", "page", "my", "has", "search", "free", "but", "our", "one", "other", "do", "no", "information", "time", "they", "site", "he", "up", "may", "what", "which", "their", "news", "out", "use", "any", "there", "see", "only", "so", "his", "when", "contact", "here", "business", "who", "web", "also", "now", "help", "get", "pm", "view", "online", "c", "e", "first", "am", "been", "would", "how", "were", "me", "s", "services", "some", "these", "click", "its", "like", "service", "x", "than", "find"]

    # mmax = 0
    # total = 0
    # for _ in range(1024):
    #     # Key comparison counts stats
    #     table = HashTable()
    #     for t in ts[:50]:
    #         table[t] = 1
        
    #     for t in ts[:50]:
    #         table.key_comparison_counts = 0
    #         table[t]
    #         mmax = max(table.key_comparison_counts, mmax)
    #         total += table.key_comparison_counts
    
    # print(mmax, total / (len(table) * 1024))