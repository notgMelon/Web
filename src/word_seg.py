import pandas as pd
import jieba
import pickle
from tqdm import tqdm
import ast
"""
    对于书籍和电影的信息进行分词
"""


word_dict = []

def contains_english(text):
    return any(char.isalpha() and char.isascii() for char in text)

class word_seg():
    def __init__(self,str) -> None:
        self.split_line(str)

    def split_line(self,str):
        # 通过 ast.literal_eval 转换为集合
        self.tags_set = ast.literal_eval(str)
        self.tags_list = self.split_long_strings()

    def split_long_strings(self):
        result = []
        length_threshold = 4
        for string in self.tags_set:
            # 如果字符串长度大于指定阈值，且不是英文
            if (len(string) > length_threshold and (not contains_english(string))):
                # 将字符串按照阈值长度分割
                parts = jieba.cut_for_search(string)
                result.extend(parts)  # 将分割后的部分添加到结果列表
            else:
                result.append(string)  # 如果字符串长度不大于阈值，直接添加到结果列表
        
        return result

def split ():

    pass


def main():
    book_tag = pd.read_csv("selected_book_top_1200_data_tag.csv")
    stopwords = {
        line.strip()
        for line in open('data/stopwords.txt', encoding='utf8').readlines()
    }
    for word in ['','\n',' ','\u3000']: # 添加额外的停用词
        stopwords.add(word)
    col_name = ['id', 'words']
    book_words = []
    #print(book_tag)
    for _,book in tqdm(book_tag.iterrows(), total=book_tag.shape[0], leave=False):
        bookline = word_seg(book["Tags"])
        key_words = bookline.tags_set
        key_words = key_words - stopwords
        book_words.append({'id': book["Book"], 'words': key_words})
    pd.DataFrame(book_words,columns=col_name).to_csv("data/book_words.csv", index=False)
    print("split book finish!")
    movie_tag = pd.read_csv("selected_movie_top_1200_data_tag.csv")
    col_name = ['id', 'words']
    movie_words = []
    for _,movie in tqdm(movie_tag.iterrows(), total=movie_tag.shape[0], leave=False):
        movieline = word_seg(movie["Tags"])
        key_words = movieline.tags_set
        key_words = key_words - stopwords
        movie_words.append({'id': movie['Movie'], 'words': key_words})
    pd.DataFrame(movie_words,columns=col_name).to_csv("data/movie_words.csv", index=False)
    with open("data/word_dict.pkl", "wb") as f:
        pickle.dump(word_dict,f)
    print("split movie finish!")

if __name__ == "__main__":
    main()