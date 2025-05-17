import boto3
import os

def upload_image_to_s3(file_path, bucket_name, object_name=None, region_name='us-east-1'):
    
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3_client = boto3.client('s3', region_name=region_name)
        with open(file_path, "rb") as f:
            s3_client.upload_fileobj(f, bucket_name, object_name)
        print(f"Upload Successful: {object_name}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    
if __name__ == "__main__":
    file_path = 'images/cat1.jpeg'  
    bucket_name = 'cats-only-bucket'
    upload_image_to_s3(file_path, bucket_name)