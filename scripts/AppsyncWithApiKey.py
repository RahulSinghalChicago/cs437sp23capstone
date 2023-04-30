import json
import boto3

s3 = boto3.client('s3')
appsync = boto3.client('appsync')
api_id = 'sxx7yrdqubdovazvfekepn5apm'
type_name = 'your-appsync-type-name'
id_field_name = 'your-appsync-id-field-name'
api_key = 'da2-ps2ujqzwfranzmzj76htprdi7i'

def lambda_handler(event, context):
    # Get the bucket and key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Get the contents of the S3 object
    obj = s3.get_object(Bucket=bucket, Key=key)
    file_content = obj['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    
    # Check if the item exists in AppSync
    query = '''
        query GetItem($id: ID!) {
            getItem(id: $id) {
                id
            }
        }
    '''
    variables = {'id': data[id_field_name]}
    response = appsync.execute_query(
        query_string=query,
        variables=variables,
        api_id=api_id,
        auth_mode='API_KEY',
        api_key=api_key
    )
    
    # Update or insert the item
    if response.get('data', {}).get(type_name):
        query = '''
            mutation UpdateItem($input: UpdateItemInput!) {
                updateItem(input: $input) {
                    id
                }
            }
        '''
        variables = {
            'input': {
                'id': data[id_field_name],
                'attribute1': data['attribute1'],
                'attribute2': data['attribute2']
            }
        }
        response = appsync.execute_mutation(
            query_string=query,
            variables=variables,
            api_id=api_id,
            auth_mode='API_KEY',
            api_key=api_key
        )
        print('Item updated in AppSync')
    else:
        query = '''
            mutation CreateItem($input: CreateItemInput!) {
                createItem(input: $input) {
                    id
                }
            }
        '''
        variables = {
            'input': {
                'id': data[id_field_name],
                'attribute1': data['attribute1'],
                'attribute2': data['attribute2']
            }
        }
        response = appsync.execute_mutation(
            query_string=query,
            variables=variables,
            api_id=api_id,
            auth_mode='API_KEY',
            api_key=api_key
        )
        print('Item inserted into AppSync')
