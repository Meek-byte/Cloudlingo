import boto3
import json
import os

s3 = boto3.client('s3')
translate = boto3.client('translate')

def lambda_handler(event, context):
    # Get the S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    try:
        # Get the file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)
        
        # Perform translation
        translated_data = {}
        for k, v in data.items():
            if isinstance(v, str) and k not in ['source_lang', 'target_lang']:
                translated_data[k] = translate.translate_text(
                    Text=v,
                    SourceLanguageCode=data['source_lang'],
                    TargetLanguageCode=data['target_lang']
                )['TranslatedText']
            else:
                translated_data[k] = v
        
        # Save to response bucket
        response_bucket = os.environ['RESPONSE_BUCKET']
        response_key = f"translated_{key}"
        s3.put_object(
            Bucket=response_bucket,
            Key=response_key,
            Body=json.dumps(translated_data, ensure_ascii=False)
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Translation completed successfully!')
        }
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing translation')
        }