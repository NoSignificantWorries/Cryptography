message = "Karpachev Dmitry"


def hash_function(p, q, message) -> int:
    n = p * q
    h = 32
    for m in message:
        m_ascii = ord(m)
        h = (h + m_ascii) ** 2 % n
    return h


print(hash_function(17, 19, message))
