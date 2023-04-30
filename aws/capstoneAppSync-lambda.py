import json
import requests
import boto3

session = boto3.Session()
appsync = session.client('appsync')

s3 = boto3.client('s3')
cognito = boto3.client('cognito-idp')
api_id = 'sxx7yrdqubdovazvfekepn5apm'
user_pool_id = 'us-east-1_wiLTn7O0L'
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
        query GetCapImage{
            getCapImage(id: "%s"){
                id
                name
                path
            }
        }
    '''
    
    filename = key.split("/")[-1]
    tokens = filename.split('_')
    
    if len(tokens) < 3:
        print(f'key is not valid {key}')
        return
    
    print(f'Filename: {filename}, {key} ')
    id = tokens[0]
    date = tokens[1]
    time = tokens[2]
    
    query = query % id
    
    print("query: ", query)

    headers = {'Authorization': access_token}
    url = 'https://bq5yzurrcfgs7o5xbqhmunq6oq.appsync-api.us-east-1.amazonaws.com/graphql'
    response = requests.post(
        url,
        json={'query': query},
        headers=headers
    )
    
    print(response.content)
    response_data = response.json().get('data', {}).get('getCapImage')
    
    print(response_data)
    # Update or insert the item
    if response_data:
        query = '''
            mutation UpdateCapImage($input: UpdateCapImageInput!) {
                updateCapImage(input: $input) {
                    id
                    name
                    path
                }
            }
        '''
        variables = {
            'input': {
                'id': response_data['id'],
                'name': response_data['name'],
                'path': key
            }
        }
        response = requests.post(
            url,
            json={'query': query, 'variables': variables},
            headers=headers
        )
        
        print(response.content)
        print('Item updated in AppSync')
    else:
        
        data = {
            'id': id,
            'name': 'UNKNOWN',
            'path': key
        }
        
        query = '''
            mutation CreateCapImage($input: CreateCapImageInput!) {
                createCapImage(input: $input) {
                    id
                }
            }
        '''
        variables = {
            'input': {
                'id': data['id'],
                'name': data['name'],
                'path': data['path']
            }
        }
        response = requests.post(
            url,
            json={'query': query, 'variables': variables},
            headers=headers
        )
        print(response.content)
        print('Item inserted into AppSync')