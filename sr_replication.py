import boto3
import logging
from config.s3_config import SOURCE_BUCKET, REGION

# Setup logging
logging.basicConfig(filename='logs/replication_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def enable_sr_replication(bucket_name, region):
    s3 = boto3.client('s3', region_name=region)

    # Set the replication configuration
    replication_config = {
        'Role': 'arn:aws:iam::YOUR_ACCOUNT_ID:role/YourReplicationRole',  # Replace with your IAM Role ARN
        'Rules': [
            {
                'ID': 'ReplicationRule1',
                'Status': 'Enabled',
                'Prefix': '',
                'Destination': {
                    'Bucket': f'arn:aws:s3:::{bucket_name}',  # Same region replication
                    'StorageClass': 'STANDARD'
                },
                'DeleteMarkerReplication': {
                    'Status': 'Disabled'
                },
            },
        ],
    }

    # Enable replication on the source bucket within the same region
    try:
        response = s3.put_bucket_replication(
            Bucket=bucket_name,
            ReplicationConfiguration=replication_config
        )
        logging.info(f"Successfully enabled SRR for bucket: {bucket_name}")
        return response
    except Exception as e:
        logging.error(f"Error enabling SRR: {e}")
        return None

if __name__ == "__main__":
    enable_sr_replication(SOURCE_BUCKET, REGION)
