import pandas as pd
import ast
import math
import csv

def get_data(file_name: str) -> dict:
    df = pd.read_csv(file_name)
    word_list = df['word'].tolist()
    id_lists = df['id_list'].tolist()
    table_list = df['skip_table'].tolist()
    return word_list,id_lists,table_list

'''    data_dic = {}
    with open(file_name, mode="r", encoding="utf8") as f:
        f_reader = csv.reader(f)
        next(f_reader)
        for row_line in f_reader:
            data_dic[row_line[0]] = [eval(row_line[1]), eval(row_line[2])]
'''    

def opti ():
    filename_book = "data/book_invert.csv"
    filename_movie = "data/movie_invert.csv"
    book_word,book_id,book_skip = get_data(filename_book)
    movie_word,movie_id,movie_skip = get_data(filename_movie)

    invert_index = []
    big_string = ""
    offset = 0
    for i in range(len(book_id)):
        id_list = ast.literal_eval(book_id[i])
        skip_list = ast.literal_eval(book_skip[i])
        if len(id_list) > 1 :
            for j in range(len(id_list) - 1, 0, -1):  # 从最后一个元素遍历到第二个元素
                id_list[j] = id_list[j] - id_list[j - 1]
        word = book_word[i]
        if word is not str:
            word= str(word)
        big_string += word
        invert_index.append({'word': offset, 'id_list': id_list, 'skip_table': skip_list})
        offset += len(word)
    pd.DataFrame(invert_index, columns=['word', 'id_list', 'skip_table']).to_csv("data/book_invert_opti.csv", index=False)
    with open('data/book_invert_opti_word.txt', 'w') as f:
        f.write(big_string)

    big_string = ""
    invert_index.clear()
    offset = 0
    for i in range(len(movie_id)):
        id_list = ast.literal_eval(movie_id[i])
        skip_list = ast.literal_eval(movie_skip[i])
        if len(id_list) > 1 :
            for j in range(len(id_list) - 1, 0, -1):  # 从最后一个元素遍历到第二个元素
                id_list[j] = id_list[j] - id_list[j - 1]
        word = movie_word[i]
        if word is not str:
            word= str(word)
        big_string += word
        invert_index.append({'word': offset, 'id_list': id_list, 'skip_table': skip_list})
        offset += len(word)
    pd.DataFrame(invert_index, columns=['word', 'id_list', 'skip_table']).to_csv("data/movie_invert_opti.csv", index=False)
    with open('data/movie_invert_opti_word.txt', 'w') as f:
        f.write(big_string)

opti()