from __future__ import print_function

import boto3
from decimal import Decimal
import json
from base64 import b64encode
import os

sagemaker_client = boto3.client('sagemaker-runtime')
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

def analyze_review(bucket, key):

    response = sagemaker_client.invoke_endpoint(
            EndpointName="hcom-sentiment-predict-endpoint",
            ContentType="application/json",
            Accept="application/json",
            Body=generateJsonBody(bucket, key)
        )

    result = json.loads(response['Body'].read().decode())
    
    print(result)
    return result

def saveResultOnTags(bucket, key, response):
    
    category = response[0]['Prediction (Sentiment)']
    confidence = str(round(response[0]['Confidence'],2))

    tag_set={
        'TagSet': [
            {
                'Key': 'sentiment-category',
                'Value': category
            },
            {
                'Key': 'confidence-level',
                'Value': confidence
            }
        ]
    }
    
    s3_client.put_object_tagging(
        Bucket=bucket,
        Key=key,
        Tagging=tag_set
    )
    print('TAGGING DONE!')
    
    moveFile(bucket, key, category)
    
    return 'TAGGING DONE!'
    
    
def moveFile(bucket, key, category):
    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': bucket,
        'Key': key
    }
    filename = os.path.basename(key)
    path = 'reviews/'+category.lower()+'/'+filename;
    print(path)
    s3.meta.client.copy(copy_source, bucket, path)
    print('FILE MOVED')
    return 'FILE MOVED'

def generateJsonBody(bucket, key):

    bucket = s3.Bucket(bucket);
    obj = bucket.Object(key).get();
    
    lines = obj['Body'].read()
    text = json.dumps(lines.decode("utf-8"))

    data =  {
            'content' :
                [{
                'text': text
                }]
            }

    data=json.dumps(data)
    print(data)
    
    return data

# --------------- Main handler ------------------

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        
        print(bucket);
        print(key);
        
        analysis_response = analyze_review(bucket, key)
        
        tag_result = saveResultOnTags (bucket, key, analysis_response)

        return 'OK'

    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e
