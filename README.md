# Capstone Project 

## Group
Rahul Singhal (rahuls11)
Anand Todkar (atodkar2)

## Code Setup

There are mainly three sections to the code.
1. Edge python code which runs on camera and Raspberry to capture and detect images
2. AWS Lambda 
3. Amplify and Flutter

### AWS Lambda
This code needs to be executed on AWS Lambda which listens to S3 event and updates dynamoDB. This file is inside `aws` folder.

### Amplify and Flutter
This code is available inside capstone_flutter. There is a lot of code but the one if interest is inside `lib/main.dart` folder. All other code is supporting logic and infrastructure.
