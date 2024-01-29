import boto3
import zipfile
from bs4 import BeautifulSoup
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

def extract_content(local_zip_path:str):
    with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
    
        for file_name in file_list:
            if file_name.endswith('.html'):
                html_content = zip_ref.read(file_name)
            
                soup = BeautifulSoup(html_content, 'html.parser')
            
                elements = soup.find_all(class_='covered_percent')
                    
                return elements[0].text

if __name__ == "__main__":
    bucket_name = 'testvini'
    object_key = 'test/hi.txt'
    local_file_path = "/home/sugan/Documents/test/coverage-2024-01-17.zip"
    coverage = extract_content(local_file_path)


    download_file_from_s3(bucket_name, object_key, local_file_path)
    process_zip_file(local_file_path)

    client = WebClient(os.environ["SLACK_BOT_TOKEN"])

    with open( "/home/sugan/Documents/test/coverage-2024-01-17.zip", 'rb') as file:
        file_contents = file.read()

        new_file = client.files_upload_v2(
            channels='C03GEKPH135',
            title=f"Coverage : {coverage}",
            filename="coverage.zip",
            file=file_contents
        )
