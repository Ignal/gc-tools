import string
import sys

letters = "mpf"

encoding_map = {}
decoding_map = {}

def capitalizeFirstLetter(s):
    if len(s) == 0:
        return s
    if len(s) == 1:
        return s[0].upper()
    return s[0].upper() + s[1:]

def getmfp(i):
    result = ""
    result += letters[i // 9]
    i %= 9
    result += letters[i // 3]
    i %= 3
    result += letters[i]
    return result

def fillMaps():
    for i in range(26):
        letter = string.ascii_lowercase[i]
        mfp = getmfp(i)
        encoding_map[letter] = mfp
        decoding_map[mfp] = letter
        encoding_map[letter.upper()] = capitalizeFirstLetter(mfp)
        decoding_map[capitalizeFirstLetter(mfp)] = letter.upper()

def encodeLetter(ch):
    if ch in encoding_map:
        return encoding_map[ch]
    return ch

def encode(text):
    result = ""
    for ch in text:
        result += encodeLetter(ch)
    return result
        

def decodeNextSequence(text):
    if len(text) < 3:
        return "", text
    seq = text[:3]
    if seq in decoding_map:
        return text[3:], decoding_map[seq]
    return text[1:], text[0] 

def decode(text):
    result = ""
    while len(text) > 0:
        text, decoded = decodeNextSequence(text)
        result += decoded
    return result

fillMaps()

text = ""
for line in sys.stdin:
    text += line

transform = encode
if len(sys.argv) > 1:
    if sys.argv[1] == "-d":
        transform = decode

print(transform(text), end = "")
