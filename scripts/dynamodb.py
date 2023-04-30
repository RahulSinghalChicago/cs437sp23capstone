import json
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = 'CapImage-sxx7yrdqubdovazvfekepn5apm-dev'

def lambda_handler(event, context):
    # Get the bucket and key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    print(event['Records'][0]['s3'])
    
    # Get the contents of the S3 object
    #obj = s3.get_object(Bucket=bucket, Key=key)
    #file_content = obj['Body'].read().decode('utf-8')
    #data = json.loads(file_content)
    
    # Check if the item exists in DynamoDB
    table = dynamodb.Table(table_name)
    
    data = {'id': '12345', 'name': 'asmita todkar', 'path': 'correct path', 'description': 'correct description jfhfjh kjhgfjh'}
    
    response = table.get_item(Key={'id': data['id']})
    
    print("response from dynamodb: ", response)
    
    # Update or insert the item
    if 'Item' in response:
        table.update_item(
            Key={'id': data['id']},
            UpdateExpression='SET description = :val2',
            ExpressionAttributeValues={
                ':val2': data['description']
            }
        )
        print('Item updated in DynamoDB')
    else:
        table.put_item(Item=data)
        print(f'Item inserted {data} into DynamoDB')
