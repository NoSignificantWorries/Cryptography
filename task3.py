# Выполнить один цикл ГОСТ 28147-89
# Взять 64 бита исходного текста (ФИО)
# Ключ 256 бит (32 буквы текста) - фраза
# Исходное сообщение бьём на две части, к первой применяем функцию и делаем побитовое сложение второй части и результата функции.
# Функция: берём правую часть и подключ (4 символа ключа), складываем побитово и по модулую берём 2^32 -> конструкция из 32 бит
# Блок подстановки, снова берём 32 бита и сдвигаем влево на 11 бит

from collections.abc import Generator

from task1 import decrypted_message

TABLE = [
    [1, 13, 4, 6, 7, 5, 14, 4],
    [15, 11, 11, 12, 13, 8, 11, 10],
    [13, 4, 10, 7, 10, 1, 4, 9],
    [0, 1, 0, 1, 1, 13, 12, 2],
    [5, 3, 7, 5, 0, 10, 6, 13],
    [7, 15, 2, 15, 8, 3, 13, 8],
    [10, 5, 1, 13, 9, 4, 15, 0],
    [4, 9, 13, 8, 15, 2, 10, 14],
    [9, 0, 3, 4, 14, 14, 2, 6],
    [2, 10, 6, 10, 4, 15, 3, 11],
    [3, 14, 8, 9, 6, 12, 8, 1],
    [14, 7, 5, 14, 12, 7, 1, 12],
    [6, 6, 9, 0, 11, 6, 0, 7],
    [11, 8, 12, 3, 2, 0, 7, 15],
    [8, 2, 15, 11, 5, 9, 5, 5],
    [12, 12, 14, 2, 3, 11, 9, 3]
]
MOD = 2 ** 32


class Bytestring:
    def __init__(self, s: str = "") -> None:
        self.bins = self._string_to_bytes(s)
        self.size = len(self.bins)

    def __str__(self) -> str:
        return f"Bins arraw (length: {self.size}) '{self.bins}'"

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, other: Bytestring) -> Bytestring:
        result = ""
        for b1, b2 in zip(self.bins, other.bins):
            b1 = bool(int(b1))
            b2 = bool(int(b2))
            result += "1" if b1 ^ b2 else "0"
        new_string = Bytestring()
        new_string.bins = result
        new_string.size = len(result)
        return new_string

    def _string_to_bytes(self, s: str) -> str:
        bytestring = ""
        for letter in s:
            num = ord(letter)
            bins = bin(num)[2:]
            bins = "0" * (8 - len(bins)) + bins
            bytestring += bins
        return bytestring

    def concat(self, other: Bytestring) -> Bytestring:
        self.bins += other.bins
        self.size += other.size
        return self

    def shift_cycle_left(self, step: int) -> Bytestring:
        p1 = self.bins[:step]
        p2 = self.bins[step:] + p1
        self.bins = p2
        return self

    def get_substring(self, start: int, end: int) -> Bytestring:
        splice = Bytestring()
        substring = self.bins[start:end]
        splice.bins = substring
        splice.size = len(substring)
        return splice

    def iter_bits(self, step: int = 1) -> Generator[Bytestring]:
        for i in range(0, self.size, step):
            new = Bytestring()
            new.bins = self.bins[i:i + step]
            new.size = step
            yield new

    def to_ascii(self) -> str:
        s = ""
        for byte in self.iter_bits(8):
            s += chr(byte.to_int())
        return s

    def to_int(self) -> int:
        return int(self.bins, 2)

    def from_int(self, number: int) -> Bytestring:
        str_number = bin(number)[2:]
        if len(str_number) > self.size:
            self.bins = str_number[:self.size]
        else:
            self.bins = "0" * (self.size - len(str_number)) + str_number
        return self


def func(r: Bytestring, key: Bytestring):
    s = (r.to_int() + key.to_int()) % MOD
    r_sum_mod = Bytestring()
    r_sum_mod.size = 32
    r_sum_mod.from_int(s)

    new_r = Bytestring()
    new_r.size = 0
    for i, block in enumerate(r_sum_mod.iter_bits(step=4)):
        t = TABLE[block.to_int()][i]
        new_block = Bytestring()
        new_block.size = 4
        new_block.from_int(t)
        new_r.concat(new_block)

    return new_r


# One way
def gost_round(block: Bytestring, sub_key: Bytestring, swap: bool = True) -> Bytestring:
    l = block.get_substring(0, 32)
    r = block.get_substring(32, 64)

    f = func(r, sub_key)
    new_l = l + f

    if swap:
        result = r.concat(new_l)
    else:
        result = new_l.concat(r)
    return result


def gost_round_inverse(block: Bytestring, sub_key: Bytestring) -> Bytestring:
    l_prime = block.get_substring(0, 32)
    r_prime = block.get_substring(32, 64)

    f_val = func(l_prime, sub_key)
    l = r_prime + f_val

    result = Bytestring()
    result = l.concat(l_prime)
    return result


def split_key(key_array: Bytestring) -> list[Bytestring]:
    return [key_array.get_substring(i * 32, (i + 1) * 32) for i in range(8)]


def round_keys_encrypt(sub_keys: list[Bytestring]) -> list[Bytestring]:
    return sub_keys * 3 + sub_keys[::-1]


def round_keys_decrypt(sub_keys: list[Bytestring]) -> list[Bytestring]:
    return round_keys_encrypt(sub_keys)[::-1]


def gost_encrypt(block, key_array):
    sub_keys = split_key(key_array)
    keys = round_keys_encrypt(sub_keys)
    for i, k in enumerate(keys):
        last = (i == 31)
        block = gost_round(block, k, swap=not last)
    return block


def gost_decrypt(block, key_array):
    sub_keys = split_key(key_array)
    keys = round_keys_decrypt(sub_keys)
    for i, k in enumerate(keys):
        last = (i == 31)
        block = gost_round(block, k, swap=not last)
    return block


msg = "Karpachev Dmitry"
msg_array = Bytestring(msg)
print(msg_array)

key = "Space cat's love beautiful soup!"
key_array = Bytestring(key)
print(key_array)

subkeys = split_key(key_array)

encrypt_keys = round_keys_encrypt(subkeys)

sub_key = encrypt_keys[0]
print(sub_key)
one_round = gost_round(msg_array.get_substring(0, 64), sub_key)
print(one_round)

# Second way
decrypt_keys = round_keys_decrypt(subkeys)
decrypted_round = gost_round_inverse(one_round, sub_key)
print(decrypted_round)
print(decrypted_round.to_ascii())

print("\n")
print(msg_array.get_substring(0, 64))
encrypted_msg = gost_encrypt(msg_array.get_substring(0, 64), key_array)
print(encrypted_msg)
decrypted_msg = gost_decrypt(encrypted_msg, key_array)
print(decrypted_msg)
print(decrypted_msg.to_ascii())
