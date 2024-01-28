import boto3
import os
import json
from urllib import request, parse
from slack_sdk import WebClient

def download_file_from_s3(bucket_name, object_key, local_file_path):
    aws_access_key_id = 'AKIASGC7GIXMXNNBMJAU'
    aws_secret_access_key = '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'
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3.download_file(bucket_name, object_key, local_file_path)


def send_slack_message(channel, message):
    slack_webhook_url = 'https://hooks.slack.com/services/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'
    
    payload = {'channel': channel, 'text': message}
    
    request.urlopen(slack_webhook_url, data=parse.urlencode({'payload': json.dumps(payload)}).encode('utf-8'))



if __name__ == "__main__":
    bucket_name = 'testvini'
    object_key = 'test/hi.txt'
    local_file_path = "/home/sugan/Documents/test/hi.txt"

    download_file_from_s3(bucket_name, object_key, local_file_path)
    # process_zip_file(local_file_path)

    client = WebClient(os.environ["SLACK_BOT_TOKEN"])

    new_file = client.files_upload_v2(
    channels='C03GEKPH135',
    title="My Test Text File",
    filename="test.txt",
    content="Hi there! This is a text file!",
)
