import boto3
from botocore.config import Config
import os

secret = os.environ.get('aws_secret_access_key')
access = os.environ.get('aws_access_key_id')

my_config = Config(region_name = 'us-east-1')

client = boto3.client(
    's3',
    aws_access_key_id=access,
    aws_secret_access_key=secret,
    config=my_config
)

# create bucket (already created 'tedi-video-bucket')
# client.create_bucket(Bucket='tedi-video-bucket')

def listBuckets(client):
    reponse = client.list_buckets()

    #output the bucket names
    print('Existing Buckets:')
    for bucket in reponse['Buckets']:
        print(f' {bucket["Name"]}')

# upload video, returns true when uploaded
# reponseForUpload = client.upload_file('../sample-mp4.mp4', 'tedi-video-bucket', 'sample-mp4.mp4')
# print(reponseForUpload)

# get pre-signed url for video
responseForURL = client.generate_presigned_url('get_object',Params={'Bucket': 'tedi-video-bucket','Key':'sample-mp4-file.mp4'},ExpiresIn=3600)
print(responseForURL)