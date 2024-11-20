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

def eval ():
    filename_book = "data/book_invert.csv"
    filename_movie = "data/movie_invert.csv"
    book_word,book_id,book_skip = get_data(filename_book)
    movie_word,movie_id,movie_skip = get_data(filename_movie)

    invert_index = []
    alone = 0
    total = len(book_id)
    for i in range(len(book_id)):
        id_list = ast.literal_eval(book_id[i])
        skip_list = ast.literal_eval(book_skip[i])
        if len(id_list) == 1 :
            alone += 1
    print("book:\n")
    print(f"倒排表的总长度（所有文档索引数的总和）: {total}\n")
    print(f"只有一个索引的词项个数: {alone}\n")
    alone_rate = alone / total
    print(f"倒排表的总长度与只有一个索引的词项个数之比: {alone_rate:.2f}\n")

    big_string = ""
    invert_index.clear()
    offset = 0
    alone = 0
    total = len(movie_id)
    for i in range(len(movie_id)):
        id_list = ast.literal_eval(movie_id[i])
        skip_list = ast.literal_eval(movie_skip[i])
        if len(id_list) == 1 :
            alone += 1
    print("movie:\n")
    print(f"倒排表的总长度（所有文档索引数的总和）: {total}\n")
    print(f"只有一个索引的词项个数: {alone}\n")
    alone_rate = alone / total
    print(f"倒排表的总长度与只有一个索引的词项个数之比: {alone_rate:.2f}\n")

eval()