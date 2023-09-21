from transformers import pipeline
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Response, jsonify
# # パイプラインの準備
# model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') 
# tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
# classifier = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)

# classifier = pipeline(
#     model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
#     top_k=1
# )
# tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512,'return_tensors':'pt'}


def analysze_emotion_exreme(text):
    emotion_dict = text["extreme"]
    labels = []
    values = []
    for e in emotion_dict:
       labels.append(e[0])
       values.append(e[1])
    # print(text_with_emotion)
    plt.cla()
    plt.rcParams['font.size'] = 30
    plt.pie(values, autopct=lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '')
    plt.legend(title = "Extreme emotions:", labels = labels, bbox_to_anchor=(0.65, 1.1), fontsize="25")
    
    png_output = BytesIO()
    plt.savefig(png_output, format='png')
    plt.cla()
    png_output.seek(0)
    headers = {'Content-Type': 'image/png'}

    try:
        # return jsonify(res)
        return Response(png_output.read(), headers=headers)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
