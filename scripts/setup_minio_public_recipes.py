#!/usr/bin/env python3
"""
Script to configure MinIO bucket policies for public access to recipes folder
"""
import os
import time
import requests
from minio import Minio
from minio.error import S3Error

def wait_for_minio():
    """Wait for MinIO to be ready"""
    print("Waiting for MinIO to be ready...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            client = Minio(
                'minio:9000',
                access_key='admin1234',
                secret_key='admin1234',
                secure=False
            )
            # Try to list buckets to test connection
            client.list_buckets()
            print("MinIO is ready!")
            return client
        except Exception as e:
            print(f"MinIO not ready yet, waiting... (attempt {retry_count + 1}/{max_retries})")
            time.sleep(2)
            retry_count += 1
    
    raise Exception("MinIO did not become ready within the timeout period")

def setup_public_recipes_policy(client):
    """Setup public read policy for recipes folder"""
    bucket_name = 'recipe-api'
    
    try:
        # Create bucket if it doesn't exist
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Created bucket: {bucket_name}")
        else:
            print(f"Bucket {bucket_name} already exists")
        
        # Set bucket policy for public read access to recipes folder only
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/recipes/*"]
                }
            ]
        }
        
        import json
        client.set_bucket_policy(bucket_name, json.dumps(policy))
        print("✅ Policy applied successfully!")
        print("✅ Images in /recipe-api/recipes/ are now publicly accessible")
        print("✅ Other folders remain private")
        
    except S3Error as e:
        print(f"Error setting up policy: {e}")
        raise

if __name__ == "__main__":
    try:
        client = wait_for_minio()
        setup_public_recipes_policy(client)
        print("🎉 MinIO configuration completed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
