#!/bin/bash

# Wait for MinIO to be ready
echo "Waiting for MinIO to be ready..."
until mc alias set myminio http://localhost:9000 admin1234 admin1234; do
  echo "MinIO not ready yet, waiting..."
  sleep 2
done

echo "MinIO is ready!"

# Create bucket if it doesn't exist
mc mb myminio/recipe-api --ignore-existing

# Create a policy for public read access to recipes folder
cat > /tmp/recipes-public-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": ["*"]
      },
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::recipe-api/recipes/*"]
    }
  ]
}
EOF

# Apply the policy
mc policy set-json /tmp/recipes-public-policy.json myminio/recipe-api

echo "Policy applied successfully!"
echo "Images in /recipe-api/recipes/ are now publicly accessible"
echo "Other folders remain private"
