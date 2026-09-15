# Выполнить один цикл ГОСТ 28147-89
# Взять 64 бита исходного текста (ФИО)
# Ключ 256 бит (32 буквы текста) - фраза
# Исходное сообщение бьём на две части, к первой применяем функцию и делаем побитовое сложение второй части и результата функции.
# Функция: берём правую часть и подключ (4 символа ключа), складываем побитово и по модулую берём 2^32 -> конструкция из 32 бит
# Блок подстановки, снова берём 32 бита и сдвигаем влево на 11 бит

from collections.abc import Generator

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
            result += "1" if b1 or b2 else "0"
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
    r_sum = r + key

    r_sum_int = r_sum.to_int()
    r_sum_int_mod = r_sum_int % MOD
    r_sum_mod = r_sum.from_int(r_sum_int_mod)

    new_r = Bytestring()
    for i, block in enumerate(r_sum_mod.iter_bits(step=4)):
        t = TABLE[block.to_int()][i]
        new_block = block.from_int(t)
        new_r.concat(new_block)

    return new_r


# One way
msg = "Karpachev Dmitry"
msg_array = Bytestring(msg)
print(msg_array)

key = "Space cat's love beautiful soup!"
key_array = Bytestring(key)
print(key_array)

l0, r0 = msg_array.get_substring(0, 32), msg_array.get_substring(32, 64)
print(l0, r0)

sub_key = key_array.get_substring(0, 32)

f1 = func(r0, sub_key)
print("f1:", f1)
r1 = f1.shift_cycle_left(11)
print("r1:", r1)


# Second way
