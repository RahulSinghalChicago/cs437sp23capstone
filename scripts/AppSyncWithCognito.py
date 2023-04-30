import json
import requests
import boto3

session = boto3.Session()
appsync = session.client('appsync')

s3 = boto3.client('s3')
cognito = boto3.client('cognito-idp')
api_id = 'sxx7yrdqubdovazvfekepn5apm'
type_name = 'CapImage'
id_field_name = 'name'
user_pool_id = 'us-east-1_wiLTn7O0L'
# client_id = 'r4nq1tehhec22v430kj5kn4ra'
client_id = '479gk3qmjc7rontvtr4pt6qk0l'

def lambda_handler(event, context):
    # Get the bucket and key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    
    # Authenticate the user
    response = cognito.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            'USERNAME': 'anand',
            'PASSWORD': 'Pass@123'
        }
    )
    access_token = response['AuthenticationResult']['AccessToken']
    print(access_token)
    
    # Check if the item exists in AppSync
    query = '''
        query GetItem($id: ID!) {
            getItem(id: $id) {
                id
            }
        }
    '''
    variables = {'id': 'name'}
    headers = {'Authorization': access_token}

   # Check if the item exists in AppSync
    query = '''
        query GetItem($id: ID!) {
            getItem(id: $id) {
                id
            }
        }
    '''
    variables = {'id': 'name'}
    headers = {'Authorization': access_token}
    url = 'https://bq5yzurrcfgs7o5xbqhmunq6oq.appsync-api.us-east-1.amazonaws.com/graphql'
    response = requests.post(
        url,
        json={'query': query, 'variables': variables},
        headers=headers
    )
    response_data = response.json().get('data', {}).get('getItem')
    
    # Update or insert the item
    if response_data:
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
        response = requests.post(
            url,
            json={'query': query, 'variables': variables},
            headers=headers
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
        response = requests.post(
            url,
            json={'query': query, 'variables': variables},
            headers=headers
        )
        print('Item inserted into AppSync')