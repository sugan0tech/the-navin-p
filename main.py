import boto3
import os
import json
import dotenv
from urllib import request, parse
from slack_sdk import WebClient
dotenv.load_dotenv()

def download_file_from_s3(bucket_name, object_key, local_file_path):
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3.download_file(bucket_name, object_key, local_file_path)

if __name__ == "__main__":
    bucket_name = 'testvini'
    object_key = 'test/hi.txt'
    local_file_path = "/home/sugan/Documents/test/hi.txt"

    download_file_from_s3(bucket_name, object_key, local_file_path)
    # process_zip_file(local_file_path)

    client = WebClient(os.environ["SLACK_BOT_TOKEN"])

    file_contents = ""

    with open(local_file_path, 'rb') as file:
        file_contents = file.read()

    new_file = client.files_upload_v2(
    channels='C03GEKPH135',
    title="Coverage",
    filename="test.txt",
    file=file_contents
)
