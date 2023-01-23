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
import ffmpeg

# connect s3
s3 = boto3.client('s3')
bucket = 'youtubeweekly' # 수정 필요

# upload file to s3 - need to add permission
def upload_file(file_name, bucket, key, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3.put_object(Bucket=bucket, Key=key+'/'+file_name)
        # response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Download video - https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/__init__.py
def download_video(video_id):
    subprocess.call('youtube-dl --rm-cache-dir', shell="True")
    url = 'https://youtube.com/watch?v=' + video_id
    output = os.path.join('/tmp/youtubevideos/', '%(title)s.%(ext)s')
    # for id in video_id:
    #video = str(url+id)
    ydl_opts = {
        'format': 'bestaudio/best[ext=mp4]',
        'outtmpl' : output,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    print(url + ': Download Completed')
        
def lambda_handler(event, context):
  
    # get the date 7 days ago 
    d = datetime.now() + relativedelta(days=-7)
    lastcall = str(d.isoformat('T'))[0:19] + 'Z'

    t = datetime.now()
    today = str(t.isoformat('T'))[0:19] + 'Z'
    
    # change current directory (default: /var/task)
    os.chdir('/tmp')
    
    # # make a directory
    if not os.path.exists(os.path.join('youtubevideos')):
       os.makedirs('youtubevideos')
       
    os.chdir('/tmp/youtubevideos')
    
    # get video id
    videoId = event['videoId']
    print(videoId);
    
    # download a video
    url = 'https://www.youtube.com/watch\?v\=' + videoId
    download_video(videoId)
    # subprocess.call('yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 '+url, shell='True')
    
    # upload video to s3 - Need multi part upload (more than 100 MB)
    tmp = os.listdir('/tmp/youtubevideos/')
    for item in tmp:
       upload_file('/tmp/youtubevideos/'+item, bucket, today, item)

    return tmp
