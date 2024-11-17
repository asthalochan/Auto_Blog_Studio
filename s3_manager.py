import boto3

class S3Manager:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, bucket_name):
        """
        Initialize the S3Manager.

        Parameters:
        - aws_access_key_id (str): AWS access key ID.
        - aws_secret_access_key (str): AWS secret access key.
        - region_name (str): AWS region name.
        - bucket_name (str): Name of the S3 bucket.
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def save_token_to_s3(self, token_path, token):
        """
        Save a token to the S3 bucket.

        Parameters:
        - token_path (str): Path in the S3 bucket to store the token.
        - token (str): The token to save.

        Returns:
        - bool: True if the token was saved successfully, False otherwise.
        """
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=token_path, Body=token)
            print(f"Token saved to S3 at '{token_path}'.")
            return True
        except Exception as e:
            print(f"Error saving token to S3: {e}")
            return False

    def load_token_from_s3(self, token_path):
        """
        Load a token from the S3 bucket.

        Parameters:
        - token_path (str): Path in the S3 bucket to retrieve the token.

        Returns:
        - str: The token if successfully retrieved, None otherwise.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=token_path)
            token = response['Body'].read().decode('utf-8')
            print(f"Token loaded from S3 at '{token_path}'.")
            return token
        except self.s3_client.exceptions.NoSuchKey:
            print(f"Token file not found in S3 at '{token_path}'.")
            return None
        except Exception as e:
            print(f"Error loading token from S3: {e}")
            return None



if __name__ == "__main__":
    # Replace with your actual AWS credentials and bucket details
    AWS_ACCESS_KEY_ID = "your_aws_access_key_id_here"
    AWS_SECRET_ACCESS_KEY = "your_aws_secret_access_key_here"
    REGION_NAME = "your_aws_region_here"
    BUCKET_NAME = "your_bucket_name_here"
    TOKEN_PATH = "refresh_token.txt"

    # Initialize S3Manager
    s3_manager = S3Manager(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME,
        bucket_name=BUCKET_NAME
    )

    # Save a token to S3
    token_to_save = "your_refresh_token_here"
    success = s3_manager.save_token_to_s3(TOKEN_PATH, token_to_save)
    if success:
        print("Token saved successfully.")

    # Load a token from S3
    loaded_token = s3_manager.load_token_from_s3(TOKEN_PATH)
    if loaded_token:
        print(f"Loaded token: {loaded_token}")
