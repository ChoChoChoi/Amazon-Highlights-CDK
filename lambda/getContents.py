# Import the packages
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from botocore.exceptions import ClientError
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import youtube_dl
import os
import boto3
import subprocess
import json


##################
# Input: YouTube API Key (str) - it's hardcoded now
# OutPut : Video Id List (json) - $.videolist
##################


# YouTube API Parameter
def build_youtube_search(developer_key):
    DEVELOPER_KEY = developer_key
    YOUTUBE_API_SERVICE_NAME="youtube"
    YOUTUBE_API_VERSION="v3"
    return build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    
# Search Parameter
def get_search_response(youtube, lastcall):
  search_response = youtube.search().list(
    order = "date",
    publishedAfter = lastcall,
    part = "snippet",
    maxResults = 10,
    channelId = "UCdoadna9HFHsxXWhafhNvKw" # AWS Events Channel
    ).execute()
  return search_response

# Convert into dict
def info_to_dict(videoId, title, description, date):
  result = {
      "videoId": videoId,
      "title": title,
      "description": description,
      "date": date
  }
  return result
  
# Get Video Info
def get_video_info(search_response):
  result_json = {}
  list = []
  for item in search_response['items']:
    if item['id']['kind'] == 'youtube#video':
      list.append(info_to_dict(item['id']['videoId'], item['snippet']['title'], item['snippet']['description'], item['snippet']['publishedAt']))
  result_json['video'] = list
  return result_json
  
# Get Video ID
def get_video_id(search_response):
    video_id = []
    for item in search_response['items']:
        video_id.append(item['id']['videoId'])
    return video_id
    

def lambda_handler(event, context):
  
    # get the date 7 days ago 
    d = datetime.now() + relativedelta(days=-7)
    lastcall = str(d.isoformat('T'))[0:19] + 'Z'
    
    # get video info
    youtube = build_youtube_search("AIzaSyAvZuCRcx7sWA-OUiPjkml_Xv3F4aNXGEc")
    video_info = get_search_response(youtube, lastcall)
    video_list = get_video_info(video_info)
    return {
      "body" : video_list
      }
