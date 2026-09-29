import math
import random


def generate_RSA(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int]]:
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = p
    while math.gcd(e, phi_n) != 1:
        e += 1

    d = e
    for di in range(e + 1, n):
        if (di * e) % phi_n == 1:
            d = di
            break

    return (d, n), (e, n)


def encrypt_message(message: str, key: tuple[int, int]) -> list[int]:
    e, n = key
    encrypted_message = [(ord(m) ** e) % n for m in message]
    return encrypted_message


def decrypt_message(encrypted_message: list[int], key: tuple[int, int]) -> str:
    d, n = key
    decrypted_message = [chr(c ** d % n) for c in encrypted_message]
    return "".join(decrypted_message)


def hash_function(p, q, message) -> int:
    n = p * q
    h = 32
    for m in message:
        m_ascii = ord(m)
        h = (h + m_ascii) ** 2 % n
    return h


def main() -> None:
    private, public = generate_RSA(17, 23)
    print("Private key:", private)
    print("Public key:", public)

    fio = "Karpachev Dmitry Aleksandrovich"
    fio_hash = hash_function(23, 29, fio)
    print(fio_hash)

    e_msg = encrypt_message(str(fio_hash), private)
    d_msg = decrypt_message(e_msg, public)
    print(e_msg)
    print(d_msg)

    print("\nfriend:")
    friend_key = (63, 253)
    friend_msg = [233, 165]
    friend_d_msg = decrypt_message(friend_msg, friend_key)
    print(friend_d_msg)


def random_money_auth() -> None:
    def func(x: int) -> int:
        ...

    alice_f = int(input("Alice f(x):"))

    rand = random.choice([0, 1])
    print("Rand:", rand)

    alice_number = int(input("Alice x:"))

    print(func(alice_number) == alice_f)


def document() -> None:
    private, public = generate_RSA(17, 23)
    print("Private key:", private)
    print("Public key:", public)

    text = "Purple rats is dancing the tango!"

    enc_msg = encrypt_message(text, private)
    print(enc_msg)


def trades_one() -> None:
    key = (1141571, 1148743)

    message = "SALE: You can buy black colored rats 15$ by one."

    print(encrypt_message(message, key))


def trades_two() -> None:
    key = (1141571, 1148743)

    messages = [
        "darova",
        "буквально 1984",
        "abob skasal privet",
        "kupi 95 benzin za 67 rublesov",
        "banan slivi hamam",
        "я люблю твою маму",
        "Я ничего не понял",
        "SALE: You can buy black colored rats 15$ by one.",
        "Пожри тортика",
        "привет из 31 группы ",
    ]
    enc_messages = [
        [773580, 914430, 453243, 1075343, 716414, 875818, 1140688, 667676, 914430, 453243, 875818, 914430, 298411, 667676, 453243, 176422, 1024785],
        [699356, 1085795, 839969, 1085795, 914430, 635086, 68340, 699356, 635086, 699356, 1119088, 914430, 468121, 565432, 1130154, 555149, 647240, 541483],
        [68340, 876000, 468121, 1130154, 914430, 986730, 1140621, 914430, 1085795, 647240, 662037, 456472, 1130154, 662037, 914430, 456472, 699356, 914430, 22887, 1002817, 914430, 565432, 876000, 1085795, 1119088, 647240, 635086, 839969, 555149],
        [1085795, 699356, 662037, 699356, 662037, 914430, 635086, 1119088, 1130154, 555149, 1130154, 914430, 725125, 699356, 554774, 699356, 554774],
        [298411, 871234, 1075343, 798055, 875818, 389027, 914430, 1075343, 636004, 914430, 173337, 493785, 914430, 1140688, 871234, 38849, 298411, 298411, 53535],
        [347588, 38849, 557309, 798055, 946654, 1024785, 1030846, 453243, 667676, 914430, 493785, 986730, 393853, 444427],
        [58418, 699356, 565432, 839969, 555149, 699356],
        [206937, 667676, 415749, 871234, 1075343, 914430, 389027, 667676, 871234, 389027, 1075343, 557309, 946654],
        [628927, 221363, 422603, 496716, 920147, 914430, 803325, 839969, 876000, 914430, 260497, 699356, 662037, 914430, 1085795, 876000, 78035, 914430, 1085795, 1119088, 699356, 260497, 68340, 914430, 260497, 839969, 1119088, 839969, 565432, 647240, 58418, 914430, 565432, 699356, 541483, 635086, 914430, 493785, 1140621, 286850, 914430, 1085795, 78035, 914430, 839969, 662037, 647240, 410260]
    ]

    for msg in enc_messages:
        dec = decrypt_message(msg, key)
        print(dec, dec in messages)


if __name__ == "__main__":
    # main()
    # random_money_auth()
    # document()
    # trades_one()
    trades_two()
