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
        if last_match in word_list:
            words.append({'valid': True, 'pos': pos, 'word': last_match, 'adj': []})
            i = words[-1]['pos']
            last_pos = pos
        else:
            words.append({'valid': False, 'pos': pos, 'word': current})
        current = ''
        last_match = ''
        continue
    # elif c == len(input_file) - 1 and (len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word'])):
    #     words.append({'valid': True, 'pos': pos, 'word': last_match, 'adj': []})
    #     last_pos = pos
    #     break
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
                words.append({'valid': True, 'pos': pos, 'word': last_match, 'adj': []})
                i = words[-1]['pos']
                current = ''
                last_match = ''
                last_pos = pos
            continue
    
    if left == 0:
        if last_match != '':
            if len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word']):
                words.append({'valid': True, 'pos': pos, 'word': last_match, 'adj': []})
                last_pos = pos
                i = words[-1]['pos']
            else:
                i = pos
        elif ever_left:
            i = pos
        current = ''
        last_match = ''

for index, dic in enumerate(words):
    last_k = len(words) - index
    if last_k > 5:
        max_k = 5
    elif last_k == 0:
        break
    else:
        max_k = last_k

    dic_len = len(dic['word'])

    for k in range(1, max_k):
        if not words[index + k]['valid']:
            if (max_k < last_k):
                max_k += 1
            continue
        
        if dic['pos'] + dic_len == words[index + k]['pos']:
            words[index]['adj'].append({'index': index + k, 'val': 1})

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

            dic_cut = dic['word'][:-len(word_l)]
            next_cut = words[index + k]['word'][len(word_l):]

            if word_l == word_r:
                # print(word_l, dic['word'], words[index + k]['word'], dic_cut, next_cut)
                if check(dic_cut) and check(next_cut):
                    words[index]['adj'].append({'index': index + k, 'val': 10, 'same': word_l})
                else:
                    found = False
                    for j in range(0, len(word_l) + 1):
                        dic_new = dic_cut
                        for x in range(0, j):
                            dic_new += word_l[x]
                        tmp = ''
                        for x in range(j, len(word_l)):
                            tmp += word_l[x]
                        next_new = tmp + next_cut
                        # print(word_l, dic_new, next_new)

                        if check(dic_new) and check(next_new):
                            words[index]['adj'].append({'index': index + k, 'val': 100, 'same': word_l})
                            found = True
                            break
                    if not found:
                        words[index]['adj'].append({'index': index + k, 'val': 1000, 'same': word_l})

            i += 1

print(words)