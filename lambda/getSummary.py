import boto3
from decimal import Decimal
import json
import urllib.request
import urllib.parse
import urllib.error
import os

# Initiate clients
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
PROJECT_ARN = os.environ['PROJECT_ARN']

print('Loading function')
print(PROJECT_ARN)

# --------------- Main handler ------------------

def lambda_handler(event, context):

    # Get the object from the event
    bucket = event['Bucket']
    key = event['Key']
    try:
        # Calls rekognition DetectLabels API to detect labels in S3 object
        response = getContents(bucket, key)
        return response

    except Exception as e:

        print(e)
        raise e

# --------------- Helper Functions to call Rekognition APIs ------------------

def getContents(bucket, key):

    try:
        response = s3.get_object(Bucket=bucket, Key=key)

        return response

    except Exception as e:

        print(e)
        raise e