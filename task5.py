# Четверичный код, 33 буквы

alphabet ="абвгдеёжзиклмнопрстуфхцчшщъыьэюя"

with open("symbols.txt", "r") as file:
    line = file.read().replace("\n", "").strip()

codes = [line[i:i+3] for i in range(0, len(line), 3)]

parts = {}
for code in codes:
    parts[code] = parts.get(code, 0) + 1

print(parts, len(parts))


def get_ngrams(codes, n=2):
    ngrams = {}
    for i in range(len(codes) - (n - 1)):
        ngram = "".join(codes[i:i+n])
        ngrams[ngram] = ngrams.get(ngram, 0) + 1
    return ngrams


def filter_ngrams(grams, threshold=1):
    for gram, freq in grams.items():
        if freq > threshold:
            print(gram, "-", freq)

filter_ngrams(get_ngrams(codes, 2))
filter_ngrams(get_ngrams(codes, 3))
filter_ngrams(get_ngrams(codes, 4))
filter_ngrams(get_ngrams(codes, 5))
filter_ngrams(get_ngrams(codes, 6))
filter_ngrams(get_ngrams(codes, 7))

keys = {
    "221": "д",
    "102": "ж",
    "320": "е",
    "212": "к",
    "000": "р",
    "301": "с",
    "122": "и",
    "020": "п",
    "022": "о",
    "120": "в",
    "210": "а",
    "110": "н",
    "220": "л",
    "201": "т",
    "200": "у",
    "011": "ю",
    "101": "ч",
    "021": "г",
    "121": "ь",
    "202": "я",
    "112": "м",
    "001": "ы",
    "300": "б",
    "010": "х",
    "222": "э",
    "230": "й",
    "302": "ш",
    "111": "ц",
    "211": "з",
    "100": "ф",
    "012": "щ"
}

for code in codes:
    dec = keys.get(code)
    if dec:
        print(dec, end="")
    else:
        print(code, end="")
