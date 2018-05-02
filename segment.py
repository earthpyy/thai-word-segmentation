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

def overlap(a, b):
    return max(i for i in range(len(b)+1) if a.endswith(b[:i]))

i = -1
while i < len(input_file) - 1:
    i += 1
    c = input_file[i]
    if c == ' ' and (len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word'])):
        if last_match in word_list:
            words.append({'valid': True, 'delete': False, 'pos': pos, 'word': last_match, 'adj': []})
            i = words[-1]['pos']
            last_pos = pos
        # else:
        #     words.append({'valid': False, 'pos': pos, 'word': current})
        current = ''
        last_match = ''
        ever_left = False
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

    if c == len(input_file) - 1:
        if check(current) and (len(words) == 0 or pos + len(current) > words[-1]['pos'] + len(words[-1]['word'])):
            words.append({'valid': True, 'delete': False, 'pos': pos, 'word': current, 'adj': []})
        elif len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word']):
            words.append({'valid': True, 'delete': False, 'pos': pos, 'word': last_match, 'adj': []})
        # TODO: valid False condition
        last_pos = pos
        break

    if check(current):
        last_match = current
        if left == 1:
            if len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word']):
                words.append({'valid': True, 'delete': False, 'pos': pos, 'word': last_match, 'adj': []})
                i = words[-1]['pos']
                current = ''
                last_match = ''
                last_pos = pos
                ever_left = False
            continue
    
    if left == 0:
        if last_match != '':
            if len(words) == 0 or pos + len(last_match) > words[-1]['pos'] + len(words[-1]['word']):
                words.append({'valid': True, 'delete': False, 'pos': pos, 'word': last_match, 'adj': []})
                last_pos = pos
                i = words[-1]['pos']
            else:
                i = pos
        elif ever_left:
            i = pos
        # else:
        #     words.append({'valid': False, 'pos': pos, 'word': current})

        current = ''
        last_match = ''
        ever_left = False

for index, dic in enumerate(words):
    if not dic['valid']:
        continue

    last_k = len(words) - index
    if last_k > 5:
        max_k = 5
    elif last_k == 0:
        break
    else:
        max_k = last_k

    dic_len = len(dic['word'])
    min_dis = 2147483647
    min_dis_i = None

    for k in range(1, max_k):
        # if not words[index + k]['valid']:
        #     if (max_k < last_k):
        #         max_k += 1
        #     continue
        
        distance = words[index + k]['pos'] - dic['pos'] - dic_len
        if distance < min_dis:
            min_dis_i = k
            min_dis = distance
        if distance == 0:
            words[index]['adj'].append({'index': index + k, 'val': 1})

        i = 0
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

                    if not found and (words[index]['pos'] + len(words[index]['word']) - len(word_l)) == words[index + k]['pos']:
                        words[index]['adj'].append({'index': index + k, 'val': 1000, 'same': word_l})

            i += 1
    
    if (min_dis > 0 and min_dis_i != None):
        unknown = ''
        for i in range(dic['pos'] + dic_len, words[index + min_dis_i]['pos']):
            unknown += input_file[i]
        words[index]['adj'] = []
        words.insert(index + 1, {'valid': False, 'pos': dic['pos'] + dic_len, 'word': unknown, 'adj': []})

# # step 3
# nodes = []
# for i, word in enumerate(words):
#     if word['valid']:
#         nodes.append({'index': i, 'adj': 0})
#         break

# i = nodes[-1]['index']
# while words[i] != words[-1]:
#     if not words[i]['adj']:
#         i += 1
#         while not words[i]['valid']:
#             i += 1
#         nodes.append({'index': i, 'adj': 0})
#     else:
#         min_adj = 1001
#         min_adj_i = -1
#         for adj in words[i]['adj']:
#             if adj['val'] < min_adj:
#                 min_adj = adj['val']
#                 min_adj_i = adj['index']
#         nodes.append({'index': min_adj_i, 'adj': min_adj})
#         i = min_adj_i

# # for nod in nodes:
# #     print(nod)

# # step 4.1.1
# for i, node in enumerate(nodes):
#     if node['adj'] == 1000:
#         same = 0
#         for adj in words[node['index'] - 1]['adj']:
#             if adj['index'] == node['index']:
#                 same = adj['same']
#                 break
#         word_l = words[node['index'] - 1]['word'][:-same]
#         word_r = words[node['index']]['word'][same:]
        
#         words.insert(node['index'] - 1, {'valid': False, 'pos': words[node['index'] - 1]['pos'], 'word': word_l, 'adj': []})
#         words.insert(node['index'], {'valid': False, 'pos': words[node['index']]['pos'], 'word': word_r, 'adj': []})
#         # TODO: can be improved
#         for i in range(node['index'] + 1, len(words)):
#             for adj in words[i]['adj']:
#                 adj['index'] += 1

# # step 4.1.3
# for index, word in enumerate(words):
#     if not word['valid']:
#         # TODO: check for correction
#         words[index - 1]['delete'] = True
#         words[index]['word'] = words[index - 1]['word'] + word['word']
#         words[index]['pos'] = words[index - 1]['pos']

# # step 4.1.4
# # for i in range(0, len(words)):
# #     if not words[i]['valid']:
# #         j = i + 1
# #         while j < len(words) - 1 and words[j]['valid']:
# #             j += 1
        
# #         same = overlap(words[i]['word'], words[j]['word'])
# #         words[j]['word'] = words[j]['word'][same:]

# for node in nodes:
#     print(words[node['index']]['word'])

# for i, word in enumerate(words):
#     print(i, word['word'], word['pos'], word['valid'])

# step 3
nodes = []
first_i = 0
for i, word in enumerate(words):
    if word['valid']:
        nodes.append({'node': word, 'adj': -1})
        first_i = i
        break

i = first_i
while words[i] != words[-1]:
    if not words[i]['adj']:
        i += 1
        while not words[i]['valid']:
            i += 1
        nodes.append({'node': words[i], 'adj': -1})
    else:
        min_adj = 1001
        min_adj_i = -1
        for j, adj in enumerate(words[i]['adj']):
            if adj['val'] < min_adj:
                min_adj = adj['val']
                min_adj_i = adj['index']
        nodes[-1]['adj'] = j
        nodes.append({'node': words[min_adj_i], 'adj': -1})
        i = min_adj_i

# for nod in nodes:
#     print(nod)

# step 4.1.1
for i, nod in enumerate(nodes):
    node = nod['node']

    if nod['adj'] >= 0 and node['adj'][nod['adj']]['val'] == 1000:
        next_node = node['adj'][nod['adj']]['index']
        same = len(node['adj'][nod['adj']]['same'])
        word_l = words[next_node - 1]['word'][:-same]
        word_r = words[next_node]['word'][same:]

        # TODO: recheck
        words[next_node - 1]['delete'] = True
        words[next_node]['delete'] = True

        words.insert(next_node - 1, {'valid': False, 'pos': words[next_node - 1]['pos'], 'word': word_l, 'adj': []})
        words.insert(next_node, {'valid': False, 'pos': words[next_node]['pos'], 'word': word_r, 'adj': []})

# step 4.1.3
for index, word in enumerate(words):
    if not word['valid']:
        # TODO: check for correction
        words[index]['word'] = words[index - 1]['word'] + word['word']
        words[index]['pos'] = words[index - 1]['pos']
        words[index - 1]['delete'] = True

# step 4.1.4
for i in range(0, len(words)):
    if not words[i]['valid']:
        j = i + 1
        while j < len(words) - 1 and words[j]['valid']:
            j += 1
        
        same = overlap(words[i]['word'], words[j]['word'])
        words[j]['word'] = words[j]['word'][same:]

keywords = []
for node in nodes:
    if not node['node']['delete']:
        keywords.append(node['node']['word'])
        if node['adj'] >= 0 and node['node']['adj'][node['adj']]['val'] == 10:
            keywords.append(node['node']['word'][:-len(node['node']['adj'][node['adj']]['same'])])
            keywords.append(words[node['node']['adj'][node['adj']]['index']]['word'])
        # elif node['node']['adj'][node['adj']]['val'] == 100:
            

# for word in words:
#     print(word)

print(keywords)