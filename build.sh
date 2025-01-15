if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

repository_name="fastapi-microservice"
image_version="1.0.1"

docker build \
 --platform="linux/amd64" \
 --file=docker/dockerfiles/app.Dockerfile \
 --tag="${repository_name}:${image_version}" .