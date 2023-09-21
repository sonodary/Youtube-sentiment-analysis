from flask import request, jsonify
from googleapiclient.discovery import build
import os


def get_video_details(data):
    video_URL = data['url']
    if "https://www.youtube.com/shorts/" in video_URL:
        video_id = video_URL[len("https://www.youtube.com/shorts/"):]
    else:
        video_id = video_URL[len("https://www.youtube.com/watch?v="):]

    try:
        youtube = build('youtube', 'v3', developerKey=os.environ.get("ACCESS_TOKEN_YOUTUBE"))
        video_request = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        )

        video_response = video_request.execute()

        title = video_response['items'][0]['snippet']['title']
        likes = video_response['items'][0]['statistics']['likeCount']
        views = video_response['items'][0]['statistics']['viewCount']
        comment = video_response['items'][0]['statistics']['commentCount']
        video_id_embed = video_id

        video_details = {
            'title': title,
            'viewCount': views,
            'likeCount': likes,
            'commentCount': comment,
            'videoId': video_id_embed
        }
        return jsonify(video_details)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
