from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from flask_cors import CORS
from video_info import get_video_details
from comment import get_video_comment
from word_cloud import create_word_cloud
from seven_sentiment_analysis import analyze_emotion_list
from extreme_sentiment_analysis import analysze_emotion_exreme

app = Flask(__name__)
CORS(app) 

@app.route('/api/video-details', methods=['POST'])
def video_details():
    data = request.get_json()
    return get_video_details(data)

@app.route('/api/video-comments', methods=['POST'])
def video_comments():
    data = request.get_json()
    return get_video_comment(data)
     
    # return get_video_comment(data)

@app.route('/api/video-comments-wordCloud', methods=['POST'])
def comment_word_cloud():
    words = request.get_json()
    return create_word_cloud(words)

@app.route('/api/comments-emotion', methods=['POST'])
def comment_emotion():
    words = request.get_json()
    return analyze_emotion_list(words)

@app.route('/api/comments-emotion-extreme', methods=['POST'])
def comment_emotion_extreme():
    words = request.get_json()
    return analysze_emotion_exreme(words)

if __name__ == '__main__':
    app.run()
