#!/bin/bash -e

SOURCE_IMAGE="${DOCKER_REPO}"
TARGET_IMAGE="${AWS_ECR_REPO}"
TARGET_IMAGE_LATEST="${TARGET_IMAGE}:latest"
TARGET_IMAGE_TAGGED="${TARGET_IMAGE}:${TRAVIS_TAG}"

DOCKER_TARGET_IMAGE="${DOCKERHUB_REPO}"
DOCKER_IMAGE_LATEST="${DOCKER_TARGET_IMAGE}:latest"
DOCKER_IMAGE_TAGGED="${DOCKER_TARGET_IMAGE}:${TRAVIS_TAG}"

pip install awscli
export PATH=$PATH:$HOME/.local/bin

aws configure set default.region ${AWS_REGION}
$(aws ecr get-login --no-include-email)

# AWS ECR
#docker tag ${SOURCE_IMAGE} ${TARGET_IMAGE_LATEST}
#docker push ${TARGET_IMAGE_LATEST}

#docker tag ${SOURCE_IMAGE} ${TARGET_IMAGE_TAGGED}
#docker push ${TARGET_IMAGE_TAGGED}

# Docker Hub
echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
docker tag ${SOURCE_IMAGE} ${DOCKER_IMAGE_LATEST}
docker push ${DOCKER_IMAGE_LATEST}

docker tag ${SOURCE_IMAGE} ${DOCKER_IMAGE_TAGGED}
docker push ${DOCKER_IMAGE_TAGGED}
