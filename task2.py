message = "Карпачев Дмитрий"

p, q = 17, 19
n = p * q

h = 30
conv = [h]
for m in message:
    m_ascii = ord(m)
    h = (h + m_ascii) ** 2 % n
    conv.append(h)

print(sum(conv))
