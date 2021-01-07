# Hash Tables

## Random stuff

- Length of table must always be of prime length
- Double hashing
- Universal hashing scheme
- Dynamic resizing when the load factor goes above a certain threshold
- Google's English Words dataset, representative set...
- Pearson's Chi Squared test:
    - $$\chi^2 = \sum\limits_{i=1}^n\frac{(O_i - E_i)^2}{E_i}$$
    - CRC 32    => Average is: 1.0001, Max is:  1.0078
    - Prime mod => Average is: 3.0980, Max is: 89.6704
- Key Comparion counts:
    - CRC 32    => {6, ave: 1.0218, max: 2}, {20, ave: 1.0469, max:  6}, {50, ave: 1.1570, max: 10}
    - Prime mod => {6, ave: 1.0016, max: 2}, {20, ave: 1.1446, max: 19}, {50, ave: 2.4902, max: 22}

## Runtime improvement

- Use CRC32 only (remove prime_mod_hash and resizing to a prime number)

# References

https://en.wikipedia.org/wiki/Cyclic_redundancy_check#CRC-32_algorithm

https://cp-algorithms.com/string/string-hashing.html

https://en.wikipedia.org/wiki/Hash_function#Testing_and_measurement

https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Deterministic_variants

https://cp-algorithms.com/algebra/primality_tests.html#toc-tgt-3
