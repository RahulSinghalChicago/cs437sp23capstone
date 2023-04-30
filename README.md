# Capstone Project - Front Porch Buddy

This project is the final capstone project for the CS437 course of the SP23 batch. The project's inspiration comes from the idea of having additional analytics on the camera that's installed on the front porch. The analytics should be able to detect faces and notify the homeowners if there are unfamiliar faces. If a familiar face, such as an angry neighbor, appears on the porch, the system should send a notification that Mr. X is at the porch and looking unusually angry/frustrated.

The core of the project is the use of face detection and face recognition, and annotations on the faces. Use AWS to further process the given image so as the notification can be sent to mobile App.

The project is focused on adding additional analytics to a camera that's installed on the front porch of a house. The camera is intended to detect faces and notify the homeowners if it detects unfamiliar faces. The system should also provide timely notifications and learn the patterns of people that are frequently on the porch. For example, if a child comes back from school every day at 4 PM, but hasn't arrived even after 4:15 PM, the system should notify the homeowner about the unusual activity.

To achieve these objectives, the project uses various computer vision techniques such as face detection, face recognition, and annotations on the faces. Face detection is the process of identifying and locating human faces in an image or a video. The system should be able to detect faces in real-time as they appear on the porch. Face recognition is the process of identifying individuals by comparing their facial features to a database of known faces. The system should be able to recognize familiar faces and distinguish them from unfamiliar faces.

Annotations on the faces refer to the process of adding additional information to the detected faces. For example, the system may annotate a face with the emotion detected on the face, such as "happy," "angry," or "sad." The system can use this information to provide additional context to the homeowners about the individuals on the porch.

Overall, the project aims to provide homeowners with additional insights into the individuals that appear on their front porch. By using computer vision techniques such as face detection, face recognition, and annotations on the faces, the system can detect unfamiliar faces, provide timely notifications, and learn patterns of people on the porch.

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

### Scripts

There are several scripts which we re used to verify and try things out. One of important script is `scripts\uploadS3.py` which is used to download images from one bucket and upload to another. This is needed as two project members were working independently on their individual AWS accounts and wanted to have a bridge between two.
