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
            words.append({'pos': pos, 'word': last_match, 'adj': []})
            i = words[-1]['pos']
            last_pos = pos
        current = ''
        last_match = ''
        continue
    elif c == len(input_file) - 1 and (len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word'])):
        words.append({'pos': pos, 'word': last_match, 'adj': []})
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
                words.append({'pos': pos, 'word': last_match, 'adj': []})
                i = words[-1]['pos']
                current = ''
                last_match = ''
                last_pos = pos
            continue
    
    if left == 0:
        if last_match != '':
            if len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word']):
                words.append({'pos': pos, 'word': last_match, 'adj': []})
                last_pos = pos
                i = words[-1]['pos']
            else:
                i = pos
        elif ever_left:
            i = pos
        current = ''
        last_match = ''

for index, dic in enumerate(words):
    max_k = len(words) - index
    if max_k > 3:
        max_k = 3
    elif max_k == 0:
        break

    dic_len = len(dic['word'])

    # for k in range(1, max_k):
    #     i = len(dic['word']) - 1
    #     n = 1
    #     same = 0

    #     while i >= 0:
    #         if n > next_len:
    #             break
            
    #         word_l = word_r = ''
    #         for j in range(i, len(dic['word'])):
    #             word_l = word_l + dic['word'][j]
    #         # print(word_l, end=' ')

    #         for j in range(0, n):
    #             word_r = word_r + words[index + k]['word'][j]
    #         # print(word_r)

    #         if n == 1 and k == 1 and word_l != word_r:
    #             words[index]['adj'].append({'index': index + k, 'val': 1})

    #         if word_l == word_r:
    #             same += 1

    #         print(word_l, word_r)

    #         if same > 0 and (word_l == dic['word'] or word_r == words[index + k]['word'] or word_l != word_r):
    #             print(word_l, word_r, dic['word'], words[index + k]['word'], dic['word'][:-same], words[index + k]['word'][same:])
    #             if check(dic['word'][:-same]) and check(words[index + k]['word'][same:]):
    #                 print('yes')

    #         n += 1
    #         i -= 1

    for k in range(1, max_k):
        i = 0
        same = 0
        next_len = len(words[index + k]['word'])

        if dic_len > next_len:
            # print('hu', end=' ')
            dic_start = dic_len - next_len
            next_start = next_len - 1
        else:
            # print('ha', end=' ')
            dic_start = 0
            next_start = dic_len - 1

        # print(dic['word'], words[index + k]['word'], dic_start, next_start)

        while i < dic_len and i < next_len:
            word_l = word_r = ''
            for j in range(dic_start + i, dic_len):
                word_l = word_l + dic['word'][j]
            # print(word_l, end=' ')

            for j in range(0, next_start - i + 1):
                word_r = word_r + words[index + k]['word'][j]
            # print(word_r)

            # if n == 1 and k == 1 and word_l != word_r:
            #     words[index]['adj'].append({'index': index + k, 'val': 1})

            # print(dic['word'], words[index + k]['word'], word_l, word_r)
            if word_l == word_r:
                # print(word_l, word_r, dic['word'], words[index + k]['word'], dic['word'][:-same], words[index + k]['word'][same:])
                if check(dic['word'][:-len(word_l)]) and check(words[index + k]['word'][len(word_l):]):
                    print('yes')

            i += 1

print(words)