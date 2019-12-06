## CS789: Cryptography

#### This repository is made up of custom cryptographic functions written as part of a course on cryptography. They were created with the intent of understanding the underlying logic, and should not be used for any real encryption/decryption.

`ciphers.py` contains classes that implement both the [El Gamal](https://en.wikipedia.org/wiki/ElGamal_encryption) and [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) ciphers. Each class has functions to initialize, encrypt, decrypt, and crack. Both take only one argument for initialization, the size (in digits) of the prime number that makes up the basis of the algorithm.

For El Gamal, the [Baby-step Giant-step](https://en.wikipedia.org/wiki/Baby-step_giant-step) algorithm for finding discrete logarithms is used to crack the encryption.

For RSA, [Pollard's Rho](https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm) factorization algorithm is used for cracking.

All utilities and helper functions can be found in crypt_helpers.py

Execute unit_tests.py script to run unit tests. Arguments are detailed below, and can also be accessed by appending `-h` to the script command.

```
$ ./unit_tests.py -h
usage: unit_tests.py [-h] [-s [SIZE]] [-a [ALL]] [-b [BREAKERS]]
                     [-c [CIPHERS]] [-u [UTILITIES]]

Solve traveling salesman problem using simulated annealing

optional arguments:
  -h, --help            show this help message and exit
  -s [SIZE], --size [SIZE]
                        the number of test loops to run for each suite,
                        default 50
  -a [ALL], --all [ALL]
                        runs all test suites, default True
  -b [BREAKERS], --breakers [BREAKERS]
                        runs just the breaker suite, default False
  -c [CIPHERS], --ciphers [CIPHERS]
                        runs just the cipher suite, including RSA and ElGamal,
                        default False
  -u [UTILITIES], --utilities [UTILITIES]
                        runs just the cryptographic helper function suite,
                        default False

```