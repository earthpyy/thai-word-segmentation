import json

input_file = open('panther.txt').read().translate({ord(c): ' ' for c in '!@#$%^&*()[]{};:,./<>?\|`~-=_+'})
word_list = json.load(open('thai-wordlist.json'))

words = {}
current = ''
last_match = ''
pos = 0
last_pos = 0

def word_left(str):
    n = 0;
    for word in word_list:
        if (word.startswith(str)):
            n += 1
    return n

def save():
    words[pos] = {}
    current = ''
    last_match = ''
    last_pos = pos

for i, c in enumerate(input_file):
    if c == ' ':
        save()
    elif ord(c) < 3585 or ord(c) > 3662:
        continue

    if (current == ''):
        pos = i

    current = current + c
    left = word_left(current)

    # print(current, left)
    # if i == 10:
    #     break

    if current in word_list:
        last_match = current
        if left == 1:
            save()

print(words)