## CS789: Cryptography

#### This repository is made up of custom cryptographic functions written as part of a course on cryptography. They were created with the intent of understanding the underlying logic, and should not be used for any real encryption/decryption.

`ciphers.py` contains classes that implement both the [El Gamal](https://en.wikipedia.org/wiki/ElGamal_encryption) and [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) ciphers. Each class has functions to initialize, encrypt, decrypt, and crack. Both take one argument for initialization, the size (in digits) of the prime number that makes up the basis of the algorithm. Optionally, each can be initialized with the publically transmitted pieces of the key hardcoded (n and e for RSA, mod, base, and public key for ElGamal). This can be useful when solely encrypting or cracking using someone else's public key.

For El Gamal, the [Baby-step Giant-step](https://en.wikipedia.org/wiki/Baby-step_giant-step) algorithm for finding discrete logarithms is used to crack the encryption.

For RSA, [Pollard's Rho](https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm) factorization algorithm is used for cracking.

Some sample uses of the classes are shown below:

```python
import ciphers

rsa = ciphers.RSA(15)
print('Alice\'s public key:')
print(rsa.n, rsa.e)
ciphertext = rsa.encrypt(123456)
decrypted = rsa.decrypt(ciphertext)
cracked = rsa.crack(ciphertext)

# To use a public key different than what was created on initialization:
cracked = rsa.crack([ciphertext], [n], [e])

elgamal = ciphers.ElGamal(15)
print('Alice\'s public key:')
print(elgamal.mod, elgamal.base, elgamal.key_pub)
key_B, ciphertext = elgamal.encrypt(123456)
decrypted = elgamal.decrypt(key_B, ciphertext)
cracked = elgamal.crack(key_B, ciphertext)

# Like above, to use a key other than what was created during initialization,
# pass the values in to crack or encrypt

cracked = elgamal.crack([key_B], [ciphertext], [mod], [base], [key_Pub])
encrypt = elgamal.encrypt([key_B], [ciphertext], [mod], [base], [key_Pub])
```

Another easy way to view the functionality included in the classes in to use the built-in test function.

```python
ciphers.RSA(7).test(12345)
```
```
Modulus    : 9996966593909
Exponent   : 1216367
Message    : 12345
Encrypted  : 7928205800298
Decrypted  : 12345
Cracked    : 12345
Crack time : 3.718854550999822 seconds
```

All utilities and helper functions can be found in crypt_helpers.py

Execute unit_tests.py script to run unit tests. Arguments are detailed below, and can also be accessed by appending `-h` to the script command.

```
$ ./unit_tests.py -h
usage: unit_tests.py [-h] [-s [SIZE]] [-a [ALL]] [-b [BREAKERS]]
                     [-c [CIPHERS]] [-u [UTILITIES]]

unit testing for ciphers.py and crypt_helpers.py

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
