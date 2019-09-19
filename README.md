# AWS SageMaker Automatic Sentiment Analisys and Tagging of Text files put in an S3 Bucket

This project is just an example of how to use AWS SageMaker to make AI prediction.
I used a free model/algorithm package available on AWS Sagemaker ( "knime-sentiment-model-package" ) to identify the sentiment (positive/negative) of a given text in English.
The project contains following folders:

-ui: NodeJS config file + AWS JS SDK + S3 Functions

-lambda: Python lambda file

-examples: text examples


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Buy a (FREE) AWS SageMaker model+algorithm and setup the endpoint
- Create the S3 Bucket in AWS 
- Create a Lambda to be triggered on the S3 Bucket Event (put)
- Setup CORS permission on Bucket
- Setup Amazon Cognito for Browser Identity management

### Installing

cd ui

npm install 

node server.js

## Running the App

Execute Installing instructions and then go to http://localhost:8080/

## Authors
Stefano Patitucci 


