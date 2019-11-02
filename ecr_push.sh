#!/bin/bash -e

SOURCE_IMAGE="${DOCKER_REPO}"
TARGET_IMAGE="${AWS_ECR_REPO}"
TARGET_IMAGE_LATEST="${TARGET_IMAGE}:latest"
TARGET_IMAGE_TAGGED="${TARGET_IMAGE}:${TRAVIS_TAG}"

pip install awscli
export PATH=$PATH:$HOME/.local/bin

aws configure set default.region ${AWS_REGION}
$(aws ecr get-login --no-include-email)

docker tag ${SOURCE_IMAGE} ${TARGET_IMAGE_LATEST}
docker push ${TARGET_IMAGE_LATEST}

docker tag ${SOURCE_IMAGE} ${TARGET_IMAGE_TAGGED}
docker push ${TARGET_IMAGE_TAGGED}
