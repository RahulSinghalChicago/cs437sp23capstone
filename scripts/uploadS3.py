import boto3
import botocore
import time

# AWS credentials for the source bucket
SOURCE_ACCESS_KEY = 'AKIAZUPEGOIS4ELN1234'
SOURCE_SECRET_KEY = 's/rrxGFxXMJo1mEVRiXcj435aCObFx8ma+kiedH+'

# S3 bucket information for the source bucket
SOURCE_BUCKET_NAME = 'cs437sp23capstone'
SOURCE_S3_REGION = 'us-east-1'

# AWS credentials for the destination bucket
DEST_ACCESS_KEY = 'AKIAI3AI7EVZFZE61234'
DEST_SECRET_KEY = '+X4L+EOs0+XZnMLt4IFKgLx71IoPKPLIJK7Oq46G'

# S3 bucket information for the destination bucket
DEST_BUCKET_NAME = 'capstone-sp23184301-dev'
DEST_S3_REGION = 'us-east-1'

# Create an S3 client for the source bucket using the source account credentials
source_session = boto3.session.Session()
source_s3 = source_session.client('s3', aws_access_key_id=SOURCE_ACCESS_KEY, aws_secret_access_key=SOURCE_SECRET_KEY, region_name=SOURCE_S3_REGION)

# Create an S3 client for the destination bucket using your account credentials
dest_session = boto3.session.Session()
dest_s3 = dest_session.client('s3', aws_access_key_id=DEST_ACCESS_KEY, aws_secret_access_key=DEST_SECRET_KEY, region_name=DEST_S3_REGION)

# Download images from the source bucket and upload to the destination bucket
for obj in source_s3.list_objects(Bucket=SOURCE_BUCKET_NAME, Prefix="secpi")['Contents']:
    try:
        # Download the object from the source bucket
        object_key = obj['Key']
        image = source_s3.get_object(Bucket=SOURCE_BUCKET_NAME, Key=object_key)['Body'].read()

        object_key = object_key.split('/')

        file_name = object_key[len(object_key) - 1]
        dest_key = f"public/{file_name}"

        # Upload the object to the destination bucket
        dest_s3.put_object(Body=image, Bucket=DEST_BUCKET_NAME, Key=dest_key)
        print(f"{dest_key} uploaded to {DEST_BUCKET_NAME}")
        time.sleep(10)

    except botocore.exceptions.ClientError as e:
        print(f"Error uploading {object_key} to {DEST_BUCKET_NAME}: {e}")
