from pypdf import PdfReader
import boto3
import urllib.parse

s3 = boto3.client('s3')
polly = boto3.client('polly')

OUTPUT_BUCKET = 'cloudspeak-output-babli'


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']

    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key']
    )

    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )

    text = ""

    # TXT files
    if key.endswith('.txt'):

        text = response['Body'].read().decode('utf-8')

    # PDF files
    elif key.endswith('.pdf'):

        pdf_path = '/tmp/input.pdf'

        with open(pdf_path, 'wb') as f:
            f.write(response['Body'].read())

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    else:

        return {
            'statusCode': 400,
            'body': 'Only TXT and PDF files are supported'
        }

    # No text found
    if len(text.strip()) == 0:

        return {
            'statusCode': 400,
            'body': 'No readable text found in document'
        }

    # Polly limit protection
    text = text[:3000]

    speech = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Aditi'
    )

    audio_stream = speech['AudioStream'].read()

    output_file = key.rsplit('.', 1)[0] + '.mp3'

    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=output_file,
        Body=audio_stream,
        ContentType='audio/mpeg'
    )

    return {
        'statusCode': 200,
        'body': f'Created {output_file}'
    }
