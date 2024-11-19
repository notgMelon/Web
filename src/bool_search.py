import csv
import pandas as pd
import math
from time import time

# 生成对应的 id 列表的倒排表和跳表指针
def generate_table(data: list):
    skip_table = []
    L = len(data)
    step = math.ceil(math.sqrt(L))  # 计算跳表的间隔
    loc = 0
    if L <= 3:
        for i in range(L):
            skip_table.append({'index': None, 'value': None})
    else:
        for i in range(L):  # 0 1 2 3 4
            if i == loc and i + step < L:
                #按一定间隔均匀分布跳表指针
                skip_table.append({'index': i + step, 'value': data[i + step]})
                loc = i+step
            else:
                skip_table.append({'index': None, 'value': None})
    return data, skip_table


# table 为这种结构, 元组内第一个元素为 id 列表, 第二个元素为该 id 对应的跳表指针
# index, value 是下标和下标对应的 id 值
# ([1007433],[{'index': None, 'value': None}])
def AndOperator(table1, table2):
    if table1 == () or table2 == ():
        return ()
    result = []
    i = j = 0
    while i < len(table1[0]) and j < len(table2[0]):
        if table1[0][i] == table2[0][j]:
            result.append(table1[0][i])
            i += 1
            j += 1
        elif table1[0][i] < table2[0][j]:
            while table1[1][i]['index'] is not None and table1[1][i]['value'] < table2[0][j]:
                i = table1[1][i]['index']
            else:
                i += 1
        else:
            while table2[1][j]['index'] is not None and table2[1][j]['value'] < table1[0][i]:
                j = table2[1][j]['index']
            else:
                j += 1
    return generate_table(result)


def OrOperator(table1, table2):
    if table1 == ():
        return table2
    elif table2 == ():
        return ()
    result = set(table1[0]) | set(table2[0])
    result = sorted(list(result))
    return generate_table(result)


def NotOperator(id_all, table):
    if table == ():
        return generate_table(id_all)
    result = set(id_all) - set(table[0])
    result = sorted(list(result))
    return generate_table(result)


def min_index(L: list[tuple]):
    index = 0
    for i in range(1, len(L)):
        if L[index][1] == -1:
            index = i
        elif L[i][1] < L[index][1] and L[i][1] != -1:
            index = i
    return index


def getPriority(operator: str):
    if operator == ")" or operator == "(":
        return 1
    elif operator == 'OR':
        return 2
    elif operator == 'AND':
        return 3
    elif operator == 'NOT':
        return 4


def calculate(element_stack: list, id_all):
    calculate_stack = []
    for i in range(0, len(element_stack)):
        if element_stack[i] != "NOT" and element_stack[i] != "AND" and element_stack[i] != "OR":
            calculate_stack.append(element_stack[i])
        elif element_stack[i] == "AND":
            elem2 = calculate_stack.pop()
            elem1 = calculate_stack.pop()
            calculate_stack.append(AndOperator(elem1, elem2))
        elif element_stack[i] == "OR":
            elem2 = calculate_stack.pop()
            elem1 = calculate_stack.pop()
            calculate_stack.append(OrOperator(elem1, elem2))
        else:
            elem1 = calculate_stack.pop()
            calculate_stack.append(NotOperator(id_all, elem1))
    return calculate_stack.pop()


def bool_operator(sentence: str, data, id_all):
    cstack = []
    operator_stack = []
    element_stack = []
    while sentence != "":
        cstack.append(("AND", sentence.find("AND")))
        cstack.append(("OR", sentence.find("OR")))
        cstack.append(("NOT", sentence.find("NOT")))
        cstack.append(("(", sentence.find("(")))
        cstack.append((")", sentence.find(")")))
        index = min_index(cstack)
        if cstack[index][1] == -1:
            if sentence in data.keys():
                element_stack.append(data[sentence])
            elif len(sentence) != 0:
                element_stack.append(())
            break
        else:
            if cstack[index][0] == "(" or len(operator_stack) == 0:
                operator_stack.append(cstack[index][0])
                if cstack[index][0] == "AND" or cstack[index][0] == "OR":
                    if sentence[0:cstack[index][1]] in data.keys():
                        element_stack.append(data[sentence[0:cstack[index][1]]])
                    elif len(sentence[0:cstack[index][1]]) != 0:
                        element_stack.append(())
                sentence = sentence[cstack[index][1] + len(cstack[index][0]):]
            elif getPriority(operator_stack[len(operator_stack) - 1]) > getPriority(cstack[index][0]):
                if cstack[index][0] == ")":
                    if sentence[0:cstack[index][1]] in data.keys():
                        element_stack.append(data[sentence[0:cstack[index][1]]])
                    elif len(sentence[0:cstack[index][1]]) != 0:#找不到对应词，忽略
                        element_stack.append(())
                    while len(operator_stack) != 0 and operator_stack[len(operator_stack) - 1] != "(":
                        element_stack.append(operator_stack.pop())
                    operator_stack.pop()
                    sentence = sentence[cstack[index][1] + len(cstack[index][0]):]
                else:
                    if cstack[index][0] == "AND" or cstack[index][0] == "OR":
                        if sentence[0:cstack[index][1]] in data.keys():
                            element_stack.append(data[sentence[0:cstack[index][1]]])
                        elif len(sentence[0:cstack[index][1]]) != 0:
                            element_stack.append(())
                    while len(operator_stack) != 0 and getPriority(
                            operator_stack[len(operator_stack) - 1]) > getPriority(
                        cstack[index][0]):
                        element_stack.append(operator_stack.pop())
                    operator_stack.append(cstack[index][0])
                    sentence = sentence[cstack[index][1] + len(cstack[index][0]):]
            else:
                if cstack[index][0] == "AND" or cstack[index][0] == "OR":
                    if sentence[0:cstack[index][1]] in data.keys():
                        element_stack.append(data[sentence[0:cstack[index][1]]])
                    elif len(sentence[0:cstack[index][1]]) != 0:
                        element_stack.append(())
                operator_stack.append(cstack[index][0])
                sentence = sentence[cstack[index][1] + len(cstack[index][0]):]
        cstack = []
    while len(operator_stack) != 0:
        element_stack.append(operator_stack.pop())
    return calculate(element_stack, id_all)


def get_data(file_name: str) -> dict:
    data_dic = {}
    with open(file_name, mode="r", encoding="utf8") as f:
        f_reader = csv.reader(f)
        next(f_reader)
        for row_line in f_reader:
            data_dic[row_line[0]] = (eval(row_line[1]), eval(row_line[2]))
    return data_dic


if __name__ == '__main__':
    print("read data, please wait a moment...")
    filename_book = "data/book_invert.csv"
    filename_movie = "data/movie_invert.csv"
    movie_id_series = pd.read_csv("data/movie_id.csv").squeeze()
    movie_id_all = movie_id_series.tolist()
    book_id_series = pd.read_csv("data/book_id.csv").squeeze()
    book_id_all = book_id_series.tolist()
    data_book = get_data(filename_book)
    data_movie = get_data(filename_movie)
    choice = int(input("选择查询类型( “1”查询书籍 “2”查询电影)\n"))
    if choice == 1:
        sentence = input("查询书籍, 请输入查询条件\n")
        start_time = time()
        result = bool_operator(sentence, data_book, book_id_all)
        end_time = time()
    elif choice == 2:
        sentence = input("查询电影, 请输入查询条件\n")
        start_time = time()
        result = bool_operator(sentence, data_movie, movie_id_all)
        end_time = time()
    else:
        result = ()
        print("输入错误")
    if result == ():
        print("无相关结果")
    else:
        print("\n")
        for i, id in enumerate(result[0]):
            print("=" * 20 + f"查询结果 {i+1} " + "=" * 20)
            print(f"ID:\n\t{id}")
        print("对于查询条件\t%s,花费时间为%fs"%(sentence,end_time-start_time))
'''
if __name__ == '__main__':
    find_book_str = '1'
    find_movie_str = '2'
    condion = ['爱情','恐怖 AND 科幻','NOT 日本','(科幻 OR 爱情) AND 恐怖']

    pass
    '''