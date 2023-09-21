from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
from flask import Response, jsonify

# checkpoint = 'cl-tohoku/bert-base-japanese-v3'
# tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# emotion_list = ['Joy', 'Sadness', 'Anticipation', 'Surprise', 'Anger', 'Fear', 'Disgust', 'Trust']
# model = AutoModelForSequenceClassification.from_pretrained("./pretrained_model/pretrained_seven")

def np_softmax(x):
    f_x = np.exp(x) / np.sum(np.exp(x))
    return f_x

def analyze_emotion(text, model, tokenizer, emotion_list):
    # 推論モードを有効化
    model.eval()

    # 入力データ変換 + 推論
    tokens = tokenizer(text, truncation=True, return_tensors="pt")
    tokens.to(model.device)
    preds = model(**tokens)
    prob = np_softmax(preds.logits.cpu().detach().numpy()[0])
    out_dict = {n: p for n, p in zip(emotion_list, prob)}

    return out_dict


def analyze_emotion_list(text_list):
    emotion_dict = text_list["eight"]
    labels = []
    values = []
    for e in emotion_dict:
       labels.append(e[0])
       values.append(e[1])
    plt.cla()
    plt.rcParams['font.size'] = 30
    plt.pie(values, autopct=lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '')
    plt.legend(title = "Eight emotions:", labels = labels, bbox_to_anchor=(0.83, 0.72), fontsize="25")
    png_output = BytesIO()
    plt.savefig(png_output, format='png')
    plt.cla()
    png_output.seek(0)
    headers = {'Content-Type': 'image/png'}

    try:
        return Response(png_output.read(), headers=headers)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
