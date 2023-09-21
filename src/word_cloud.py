# import matplotlib.pyplot as plt
import Mecab

def create_word_cloud(text): 
    #単語の分割
    m = MeCab.Tagger ("-Ochasen")

    # 形態素解析
    for e in text:
        node = m.parseToNode(e)
        # words=[]
        word=""
        while node:
            # node.feature：CSVで表記された素性情報を取得
            # print(node.feature)
            hinshi = node.feature.split(",")[0]
            print(hinshi)
            if hinshi in ["名詞","動詞","形容詞"]:
                origin = node.feature.split(",")[6]
                word = word + " " + origin   
            node = node.next  # 書き忘れると無限ループになるので注意

    # # wordcloudで可視化
    # fpath = "./ipaexg.ttf"
    # wordcloud = WordCloud(background_color="white",font_path=fpath, width=600,height=400,min_font_size=15)
    # wordcloud.generate(word)

    # fig = plt.figure(figsize=(12,12))
    # plt.imshow(wordcloud)
    # plt.axis('off') #軸の表示を消す
    # fig.savefig(png_output, format='png')
    return word

    
