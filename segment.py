import json

file_name = 'test.txt'
input_file = open(file_name).read().translate({ord(c): ' ' for c in '!@#$%^&*()[]{};:,./<>?\|`~-=_+"'})
word_list = json.load(open('thai-wordlist.json'))

words = []
current = ''
last_match = ''
ever_left = False
pos = 0
last_pos = 0

def word_left(str):
    n = 0;
    for word in word_list:
        if (word.startswith(str)):
            n += 1
    return n

def check(str):
    return str in word_list

i = -1
while i < len(input_file) - 1:
    i += 1
    c = input_file[i]
    if c == ' ' and (len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word'])):
        if current in word_list:
            words.append({'pos': pos, 'word': last_match})
            i = words[-1]['pos']
            last_pos = pos
        current = ''
        last_match = ''
        continue
    elif c == len(input_file) - 1 and (len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word'])):
        words.append({'pos': pos, 'word': last_match})
        last_pos = pos
        break
    elif ord(c) < 3585 or ord(c) > 3662:
        continue

    if (current == ''):
        pos = i

    current = current + c
    left = word_left(current)
    if (left > 0):
        ever_left = True

    # print(i, current, left)
    # if i == 10:
    #     break

    if check(current):
        last_match = current
        if left == 1:
            if len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word']):
                words.append({'pos': pos, 'word': last_match})
                i = words[-1]['pos']
                current = ''
                last_match = ''
                last_pos = pos
            continue
    
    if left == 0:
        if last_match != '':
            if len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word']):
                words.append({'pos': pos, 'word': last_match})
                last_pos = pos
                i = words[-1]['pos']
            else:
                i = pos
        elif ever_left:
            i = pos
        current = ''
        last_match = ''

for index, dic in enumerate(words):
    i = len(dic['word']) - 1
    if index < len(words) - 1:
        ii = len(words[index + 1]['word']) - 1
    while i >= 0 and ii >= 0:
        word_l = word_r = ''
        for j in range(i, len(dic['word'])):
            word_l = word_l + dic['word'][j]
        # print(word_l, end=' ')

        if index < len(words) - 1:
            for j in range(0, len(words[index + 1]['word']) - ii):
                word_r = word_r + words[index + 1]['word'][j]
            # print(word_r)

        i -= 1
        ii -= 1

# print(words)