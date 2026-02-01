#! /bin/bash

echo "====================================="
echo " AWS ECR Deployment Script  "
echo "====================================="
echo ""
echo "Please select deployment environment:"
echo "1) dev"
echo "2) prod"
echo "-------------------------------------"
read -p "Enter your choice (1 or 2): " deploy_stage

# Convert numeric choice to environment name
if [ "$deploy_stage" = "1" ]; then
    deploy_stage="dev"
elif [ "$deploy_stage" = "2" ]; then
    deploy_stage="prod"
else
    echo "Invalid selection. Please choose 1 for dev or 2 for prod. Exiting..."
    exit 1
fi

if [ ! -e .env ]; then
    echo ".env file not found. Exiting..."
    exit 1
fi

echo "Deploying to ${deploy_stage} environment..."
echo "====================================="

# Load Environment Variables
if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

# Export AWS credentials from .env
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
export AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}

# Authenticate with AWS ECR and login to Docker
echo "Authenticating with AWS ECR..."
aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${ECR_PUBLIC_URL}

# Repository name based on stage
repository_name="dev-retech-frontend"
image_version=$IMAGE_VERSION

export IMAGE_NAME="${repository_name}"
export IMAGE_TAG="${image_version}"

echo "Building Docker image..."
echo "====================================="
docker build \
 --platform="linux/amd64" \
 --file=docker/dockerfiles/app.Dockerfile \
 --tag="${repository_name}:${image_version}" .

echo "Tagging Docker image..."
echo "====================================="
docker tag "${repository_name}:${image_version}" "${ECR_PUBLIC_URL}/${repository_name}:${image_version}"

echo "Pushing Docker image to ECR..."
echo "====================================="
docker push "${ECR_PUBLIC_URL}/${repository_name}:${image_version}"

echo "Tagging Docker image as latest..."
echo "====================================="
docker tag "${ECR_PUBLIC_URL}/${repository_name}:${image_version}" "${ECR_PUBLIC_URL}/${repository_name}:latest"

echo "Pushing Docker image as latest..."
echo "====================================="
docker push "${ECR_PUBLIC_URL}/${repository_name}:latest"
