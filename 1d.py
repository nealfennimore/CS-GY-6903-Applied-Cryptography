import gmpy2
import string
from typing import List, Tuple
import math

Coefficients = Tuple[int, int]
Keyspace = List[str]

def decrypt(ciphertext: str, coefficients: Coefficients, keyspace: Keyspace) -> str:
    n = len(keyspace)
    a,b = coefficients

    def inverse(a, n) -> int:
        import math

        possible = [ a for a in range(n) if math.gcd(a, n) == 1]
        for p in possible:
            if (a * p) % n == 1:
                return p
            
        raise ValueError(f'No inverse for {a} mod {n}')
    
    ciphertext_words: List[str] = ciphertext.split(' ')
    plaintext_words: List[str] = []
    a_inverse = inverse(a, n)

    for word in ciphertext_words:
        indicies = [ keyspace.index(p) for p in word ]
        plaintext_words.append(
            ''.join(keyspace[(a_inverse * (idx - b)) % n] for idx in indicies)
        )

    return ' '.join(plaintext_words)

keyspace: Keyspace = list(string.ascii_uppercase)

ciphertext = 'QJKES REOGH GXXRE OXEO'
n = len(keyspace)

def are_relatively_prime(a, b):
  if a == 0 or b == 0:
    return False
  else:
    while b != 0:
      a, b = b, a % b
    return a == 1

# Find all possible A (since limited to relitively prime numbers with regards to len(keyspace))
def get_possible_a(keyspace: Keyspace) -> List[str]:
    possible_a = []
    for a in range(n):
        if are_relatively_prime(a, n) and a != 1:
            possible_a.append(a)

    return possible_a

def get_a_b(first_plain, first_cipher, second_plain, second_cipher) -> Coefficients:
  for a in get_possible_a(keyspace):
      for b in range(n):
        first = (a * keyspace.index(first_plain) + b) % n
        second = (a * keyspace.index(second_plain) + b) % n
        if first == keyspace.index(first_cipher) and second == keyspace.index(second_cipher):
            return(a,b)

coefficients = get_a_b('T','H','O','E')
decrypted = decrypt(ciphertext, coefficients, keyspace)
print(decrypted)
assert(decrypted == "IFYOU BOWAT ALLBO WLOW")