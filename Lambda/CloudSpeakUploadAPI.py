import json
import boto3
import base64
import uuid

s3 = boto3.client('s3')

INPUT_BUCKET = "cloudspeak-input-babli"

def lambda_handler(event, context):

    try:
        body = json.loads(event['body'])

        file_name = body['fileName']
        file_content = body['fileContent']

        decoded_file = base64.b64decode(file_content)

        unique_name = f"{uuid.uuid4()}_{file_name}"

        s3.put_object(
            Bucket=INPUT_BUCKET,
            Key=unique_name,
            Body=decoded_file
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Upload successful",
                "file": unique_name,
                "audioFile":unique_name.rsplit('.', 1)[0] + '.mp3',
                "audioURL":f"https://cloudspeak-output-babli.s3.ap-southeast-2.amazonaws.com/{unique_name.replace('.pdf','.mp3')}"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
