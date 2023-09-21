from googleapiclient.discovery import build
from flask import jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from seven_sentiment_analysis import analyze_emotion
import os
from dotenv import load_dotenv

load_dotenv('.env') 

extreme_emotion_dict = dict.fromkeys(["positive", "negative", "neutral"], 0)

def get_video_comment(data):
    api_key = os.environ.get("ACCESS_TOKEN_YOUTUBE")
    youtube = build('youtube', 'v3', developerKey=api_key)  

    # Extreme emotions setting up
    classifier = pipeline(
        model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
        top_k=1
    )
    # tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512,'return_tensors':'pt'}

    # Eight emotions setting up
    checkpoint = 'cl-tohoku/bert-base-japanese-v3'
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    eight_emotion_list = ['Joy', 'Sadness', 'Anticipation', 'Surprise', 'Anger', 'Fear', 'Disgust', 'Trust']
    eight_emotion_model = AutoModelForSequenceClassification.from_pretrained("./pretrained_model/pretrained_seven")
    
    # Enter video id
    video_URL = data["url"]

    if "https://www.youtube.com/shorts/" in video_URL:
        video_id = video_URL[len("https://www.youtube.com/shorts/"):]
    elif "https://www.youtube.com/watch?v=" in video_URL:
        video_id = video_URL[len("https://www.youtube.com/watch?v="):]
    else:
        print("Invalid video")
    
    # Call the API to get comments  
    try:
        comments = [[], [], [], [], []]  
        comments_dict = {}
        results = youtube.commentThreads().list(  
            part = 'snippet',  
            videoId = video_id,  
            textFormat = 'plainText',  
            ).execute()  
        
        # Loop through each comment and append to comments list  
        while results:  
            for item in results['items']:  
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments[0].append(comment) 
                likeCount = item['snippet']['topLevelComment']['snippet']['likeCount']
                comments[1].append(likeCount)  
                updatedAt = item['snippet']['topLevelComment']['snippet']['updatedAt']
                updatedAt = updatedAt[:10]+ " " + updatedAt[11:19]
                comments[2].append(updatedAt)  
                extreme = classifier(comment)
                # Get the most intensive one
                extreme_emotion = extreme[0][0]["label"]
                comments[3].append(extreme_emotion) 
                eight = analyze_emotion(comment, eight_emotion_model, tokenizer, eight_emotion_list)
                tmp = 0
                for key, value in eight.items():
                    if value >= tmp:
                        tmp = value
                        eight_emotion = key
                comments[4].append(eight_emotion) 
            # Check if there are more comments and continue iterating  
            if 'nextPageToken' in results:  
                results = youtube.commentThreads().list(  
                    part = 'snippet',  
                    videoId = video_id,  
                    textFormat = 'plainText',  
                    pageToken = results['nextPageToken']  
                ).execute()  
            else:  
                break  
        for i in range(len(comments[0])):
            comments_dict[i] = {"comment": comments[0][i], 
                                "likeCount": comments[1][i],
                                "updatedAt": comments[2][i], 
                                "extremeEmotion": comments[3][i],
                                "eightEmotion": comments[4][i]
                                }

#   {
#       name: 'コメント',
#       selector: row => row.title,
#       sortable: true,
#   },
#   {
#       name: 'ポジ/ネガ/中立',
#       selector: row => row.year,
#       sortable: true,
#   },
#   {
#     name: '感情分類',
#     selector: row => row.title,
#     sortable: true,
# },
# {
#     name: 'いいね数',
#     selector: row => row.year,
#     sortable: true,
# },
# {
#   name: '投稿時間',
#   selector: row => row.year,
#   sortable: true,
# }
# ];

        return jsonify(comments_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
