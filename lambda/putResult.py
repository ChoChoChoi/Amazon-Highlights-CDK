import boto3
import json
import os
import urllib.request
import datetime
from decimal import Decimal

DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']
REGION = os.environ['REGION']

# Initiate clients
dynamodb = boto3.resource('dynamodb', region_name=REGION)

def lambda_handler(event, context):

    payload = event
    timestamp = datetime.datetime.now().isoformat()

    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    item = {}
    
    item['DateTime'] = timestamp
    item['title'] = payload['title']
    item['tag'] = payload['tag']
    item['link'] = payload['link']

    try:
        # write the record to the database
        response = table.put_item(Item=item)
        return response

    except Exception as e:
        print(e)
        raise e