import copy
import gzip
import json

import pandas as pd
import csv

movie_tags = pd.read_csv("Movie_tag.csv")
movie = {}
for i in range(len(movie_tags)):
    movie[movie_tags["id"][i]] = movie_tags['tag'][i]

# print(movie.keys())

movie_entity = {}
with open('douban2fb.txt', 'rb') as f:
    for line in f:
        line = line.strip()
        list1 = line.decode().split('\t')
        # print(list1)
        movie_entity[list1[1]] = int(list1[0])

movies_2 = {}
with open('movie_id_map.txt', 'rb') as f:
    for line in f:
        line = line.strip()
        list1 = line.decode().split('\t')
        # print(list1)
        movies_2[int(list1[0])] = int(list1[1])

fr2int = {}
for key in movie_entity.keys():
    fr2int[key] = movies_2[movie_entity[key]]
# fr->id->int

involve = {}
tail = {}
triples = {}
for key in movie_entity.keys():
    triples[key] = []
    involve[key] = 0
    tail[key] = []
    #tail 列表存放key作为尾实体的三元组对应的头实体
    #involve 存放实体在三元组中的出现次数

with gzip.open('freebase_douban.gz', 'rb') as f:
    i = 0
    for line in f:
        i = i + 1
        if i % 10000000 == 0:
            print(i)
        line = line.strip()
        list1 = line.decode().split('\t')
        patten_str = r"<http://rdf.freebase.com/ns/"
        if (patten_str not in list1[0]) or (patten_str not in list1[2]):
            continue
        word = list1[0][len(patten_str):].strip('>')
        word2 = list1[2][len(patten_str):].strip('>')
        if word in movie_entity.keys():
            triples[word].append([list1[1], word2])
            involve[word] += 1
            if word2 not in involve.keys():
                involve[word2] = 1
                tail[word2] = [word]
            else:
                involve[word2] += 1
                if word2 not in tail.keys():
                    tail[word2] = [word]
                if word not in tail[word2]:
                    tail[word2].append(word)
        elif word2 in movie_entity.keys():
            triples[word] = []
            triples[word].append([list1[1], word2])
            involve[word] = 1
            involve[word2] += 1
            if word2 not in tail.keys():
                tail[word2] = [word]
            if word not in tail[word2]:
                tail[word2].append(word)
        # print(list1)
        # if i == 10000000:
        #     break

# graph opt
# 过滤涉及的三元组少于10个的
opt = False
if opt:
    for entity, count in list(involve.items()):
        if count < 10:
            # 从 triples 中删除该实体作为头实体的所有三元组
            if entity in triples:
                for list in triples[entity]:
                # 更新 tail 字典，删除尾实体对应的头实体引用
                    tail_entity = list[1]
                    # 删除该头实体在 tail 中的记录
                    tail[tail_entity] = [t for t in tail[tail_entity] if t != entity]
                del triples[entity]

            # 从 tail 中删除该实体作为尾实体的所有三元组
            if entity in tail:
                # 删除 tail 中与该实体相关的三元组
                for head in tail[entity]:
                    # 遍历删除对应的三元组
                    triples[head] = [t for t in triples[head] if t[1] != entity]
                del tail[entity]

            # 同时在 involve 中删除该实体
            del involve[entity]

data = json.dumps(triples, indent=1)
# print(data)
with open('knowledge_graph.json', 'w', newline='\n') as f:
    f.write(data)

# with open("knowledge_graph.json", 'r') as f:
#     triples = json.load(f)

kg_final = []
relation_dict = {}
for key1 in triples.keys():
    list1 = triples[key1]
    if key1 not in fr2int.keys():
        fr2int[key1] = len(fr2int.keys())
    for list2 in list1:
        relation1 = list2[0]
        tail_entity = list2[1]
        if relation1 not in relation_dict.keys():
            relation_dict[relation1] = len(relation_dict.keys())
        if tail_entity not in fr2int.keys():
            fr2int[tail_entity] = len(fr2int.keys())
            # print(len(movies.keys()))
        kg_final.append([fr2int[key1], relation_dict[relation1], fr2int[tail_entity]])

unique_set = set(tuple(t) for t in kg_final)

unique_set = [list(t) for t in unique_set]
# set1 = set(kg_final)
with open('baseline/data/Douban/kg_final.txt', 'w') as f:
    for list1 in unique_set:
        f.write(str(list1[0]))
        f.write(" ")
        f.write(str(list1[1]))
        f.write(" ")
        f.write(str(list1[2]))
        f.write("\n")