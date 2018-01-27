# -*- coding: utf-8 -*- #

import jieba
import jieba.posseg as pseg
import jieba.analyse
import word2vec
import gensim.models.word2vec as w2v
import redis
import re
re_english_words = re.compile(u"[a-zA-Z]+")

def getSrc():
    DB = redis.Redis(host='47.94.251.202', port=6379, db=0, password='wscjxky')
    re_chinese_words = re.compile(u"[\u4e00-\u9fa5]+")
    keys=DB.keys()
    with open('source.txt','w') as f:
        for key in keys:
            if re_chinese_words.search( str(key, encoding='utf-8'), 0):
                print( str(key, encoding='utf-8'))
                h_key=DB.hgetall(key)
                for h_k in h_key:
                    f.write(str(DB.hget(key,h_k), encoding='utf-8'))
def fenci():
    # clean file
    # with open('source.txt', 'r') as f:
    #     with open('clean.txt', 'w') as c:
    #         lines = f.readlines()
    #         for l in lines:
    #             if l!='\n':
    #                 if not re_english_words.search(l, 0):
    #                     c.write(l)

    with open('clean.txt', 'r') as f:
        with open('fenci.txt', 'w') as c:
            for l in f.readlines():
                seg=pseg.cut(l)
                seg_sentense=''
                for i,flag in seg:
                    if 'n' in flag:
                        seg_sentense+=i+' '
                c.write(seg_sentense)
    ##关键词提取，参数setence对应str1为待提取的文本,topK对应2为返回几个TF/IDF权重最大的关键词，默认值为20
    # with open('source.txt', 'r') as c:
    #     tfidf = jieba.analyse.extract_tags(c.read(), 100, withWeight=True, )
    #     for i in tfidf:
    #         print(i)
    # print(tfidf)
def word2vecModel():
    model_file_name = 'songs_model.model'
    # 模型训练，生成词向量
    sentences = w2v.LineSentence('fenci.txt')
    model = w2v.Word2Vec(sentences, size=20, window=5, min_count=10, workers=4)
    model.save(model_file_name)

if __name__ == '__main__':
    import word2vec
    # print (word2vec.doc2vec('fenci.txt','out/txt'))
    # fenci()
    model_file='text.model.syn0.npy'
    model=     word2vec.load(model_file)


