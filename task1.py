import math


def generate_RSA(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int]]:
    n = p * q
    phi_n = (p - 1) * (q - 1)
    print(phi_n)

    # e < n & d * e = 1(mod(n))
    # else: d * e mod phi(n) = 1

    e = p
    while math.gcd(e, phi_n) != 1:
        e += 1

    d = e
    for di in range(e + 1, n):
        if (di * e) % phi_n == 1:
            d = di
            break

    return (d, n), (e, n)


private, public = generate_RSA(17, 23)
print("Private key:", private)
print("Public key:", public)


def encrypt_message(message: str, key: tuple[int, int]) -> list[int]:
    e, n = key
    encrypted_message = [(ord(m) ** e) % n for m in message]
    return encrypted_message


def decrypt_message(encrypted_message: list[int], key: tuple[int, int]) -> str:
    d, n = key
    decrypted_message = [chr((c ** d) % n) for c in encrypted_message]
    return "".join(decrypted_message)


message = "Hello NSU :3"
print([ord(m) for m in message])
encrypted_message = encrypt_message(message, private)
print(encrypted_message)
decrypted_message = decrypt_message(encrypted_message, public)
print(decrypted_message)


friend_key = (63, 253)
from_friend = [44, 105, 121, 57, 73, 137]
print("From friend:", decrypt_message(from_friend, friend_key))
