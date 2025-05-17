import boto3
import json
import urllib.parse

# Initialize AWS SDK clients
s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
sns_client = boto3.client('sns')

# Configuration
SNS_TOPIC_ARN = 'Your SNS Topic ARN here'
ALLOWED_LABEL = 'Cat'
CONFIDENCE_THRESHOLD = 90.0

def lambda_handler(event, context):
    # Extract bucket and key from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    try:
        # Use AWS SDK to call Rekognition
        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=5,
            MinConfidence=CONFIDENCE_THRESHOLD
        )
        
        # Check labels
        labels = [label['Name'] for label in response['Labels']]
        is_cat_image = ALLOWED_LABEL in labels
        
        # If not a cat image, send SNS alert
        if not is_cat_image:
            message = f"Non-cat image detected in s3://{bucket}/{key}\nLabels: {', '.join(labels)}"
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject='Non-Cat Image Alert'
            )
            print(f"Alert sent: {message}")
        else:
            print(f"Cat image detected: {key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Image processed successfully')
        }
    
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        raise e