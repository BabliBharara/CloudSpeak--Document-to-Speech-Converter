# CloudSpeak – Document-to-Speech Converter

CloudSpeak is a serverless AWS application that converts PDF documents into speech and generates downloadable MP3 audio files.

## Features

- Upload PDF documents
- Automatic text extraction
- Speech generation using Amazon Polly
- MP3 playback and download
- Serverless architecture

## AWS Services Used

- Amazon S3
- AWS Lambda
- Amazon Polly
- API Gateway

## Architecture

User → Website → API Gateway → Lambda → S3 Input Bucket → Polly → S3 Output Bucket → MP3

## Technologies

- HTML
- CSS
- JavaScript
- Python
- AWS
