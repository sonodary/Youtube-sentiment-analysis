import MeCab
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
# from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
from flask import Response, jsonify

# 解析したい文章
def create_word_cloud(text): 
    #単語の分割
    matplotlib.use('agg')
    text = text["commentsList"]
    m = MeCab.Tagger("-Owakati")
    # 形態素解析
    node = m.parseToNode("".join(text))
    words=[]
    word=""
    while node:
        # node.feature：CSVで表記された素性情報を取得
        # print(node.feature)
        hinshi = node.feature.split(",")[0]
        if hinshi in ["名詞","動詞","形容詞"]:
            origin = node.surface
            word = word + " " + origin   
        node = node.next  # 書き忘れると無限ループになるので注意
    
     # wordcloudで可視化
    fpath = "./font/SourceHanSerifK-Light.otf"
    wordcloud = WordCloud(background_color="white",font_path=fpath, width=600,height=600,min_font_size=15)
    wordcloud.generate(word)

    # fig = plt.figure(figsize=(12,12))
    plt.cla()
    plt.figure(figsize=(15,15))
    plt.imshow(wordcloud)
    plt.axis('off') #軸の表示を消す
    png_output = BytesIO()
    plt.savefig(png_output, format='png')
    plt.cla()
    png_output.seek(0)
    headers = {'Content-Type': 'image/png'}
    try:
        return Response(png_output.read(), headers=headers)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

   

    
