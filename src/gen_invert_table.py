import pandas as pd
import ast
import math

def read_csv():
    book_data = pd.read_csv("data/book_words.csv", dtype={'id': int, 'words': str})
    # print(book_data.head())
    data = book_data
    words_all_book = set()
    book = dict()
    for i in range(len(data)):
        words_a_book = ast.literal_eval(data['words'][i])
        book[int(data['id'][i])] = words_a_book
        words_all_book = words_all_book.union(words_a_book)

    movie_data = pd.read_csv("data/movie_words.csv", dtype={'id': int, 'words': str})
    data = movie_data
    words_all_movie = set()
    movie = dict()
    for i in range(len(data)):
        words_a_movie = ast.literal_eval(data['words'][i])
        movie[int(data['id'][i])] = words_a_movie
        words_all_movie = words_all_movie.union(words_a_movie)

    return words_all_book, book, words_all_movie, movie


def gen_invert_table():
    invert_index = []
    words_all_book, book, words_all_movie, movie = read_csv()
    for b in words_all_book:
        temp = []
        skip_table = []
        for j in book.keys():
            field = book[j]
            if b in field:
                temp.append(j)

        temp_sorted = sorted(temp)
        L = len(temp_sorted)
        step = math.ceil(math.sqrt(L))  # 计算跳表的间隔
        loc = 0
        if L <= 3:
            for i in range(L):
                skip_table.append({'index': None, 'value': None})
        else:
            for i in range(L):
                if i == loc and i + step < L:
                    #按一定间隔均匀分布跳表指针
                    skip_table.append({'index': i + step, 'value': temp_sorted[i + step]})
                    loc = i+step
                else:
                    skip_table.append({'index': None, 'value': None})

        invert_index.append({'word': b, 'id_list': temp_sorted, 'skip_table': skip_table})
    pd.DataFrame(invert_index, columns=['word', 'id_list', 'skip_table']).to_csv("data/book_invert.csv", index=False)

    invert_index = []
    for b in words_all_movie:
        temp = []
        skip_table = []
        for j in movie.keys():
            field = movie[j]
            if b in field:
                temp.append(j)

        temp_sorted = sorted(temp)
        L = len(temp_sorted)
        step = math.ceil(math.sqrt(L))  # 计算跳表的间隔
        loc = 0
        if L <= 3:
            for i in range(L):
                skip_table.append({'index': None, 'value': None})
        else:
            for i in range(L):  # 0 1 2 3 4
                if i == loc and i + step < L:
                    #按一定间隔均匀分布跳表指针
                    skip_table.append({'index': i + step, 'value': temp_sorted[i + step]})
                    loc = i+step
                else:
                    skip_table.append({'index': None, 'value': None})

        invert_index.append({'word': b, 'id_list': temp_sorted, 'skip_table': skip_table})
    pd.DataFrame(invert_index, columns=['word', 'id_list', 'skip_table']).to_csv("data/movie_invert.csv", index=False)
    # print(invert_index)


gen_invert_table()