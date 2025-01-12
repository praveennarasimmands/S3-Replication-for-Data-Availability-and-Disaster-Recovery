import boto3
import logging
from config.s3_config import SOURCE_BUCKET, DESTINATION_BUCKET, SOURCE_REGION, DESTINATION_REGION

# Setup logging
logging.basicConfig(filename='logs/replication_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def enable_cr_replication(source_bucket, destination_bucket, source_region, destination_region):
    s3 = boto3.client('s3', region_name=source_region)

    # Set the replication configuration
    replication_config = {
        'Role': 'arn:aws:iam::YOUR_ACCOUNT_ID:role/YourReplicationRole',  # Replace with your IAM Role ARN
        'Rules': [
            {
                'ID': 'ReplicationRule1',
                'Status': 'Enabled',
                'Prefix': '',
                'Destination': {
                    'Bucket': f'arn:aws:s3:::{destination_bucket}',
                    'StorageClass': 'STANDARD'
                },
                'DeleteMarkerReplication': {
                    'Status': 'Disabled'
                },
            },
        ],
    }

    # Enable replication on the source bucket
    try:
        response = s3.put_bucket_replication(
            Bucket=source_bucket,
            ReplicationConfiguration=replication_config
        )
        logging.info(f"Successfully enabled CRR from {source_bucket} to {destination_bucket}")
        return response
    except Exception as e:
        logging.error(f"Error enabling CRR: {e}")
        return None

if __name__ == "__main__":
    enable_cr_replication(SOURCE_BUCKET, DESTINATION_BUCKET, SOURCE_REGION, DESTINATION_REGION)
