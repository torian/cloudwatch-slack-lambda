
PYTHON_VERSION=${PYTHON_VERSION:-2.7}
PROJECT_NAME=cloudwatch-slack-lambda
BUILD_PREFIX=./build

AWS_REGION=${AWS_REGION:-us-east-1}
AWS_PROFILE=${AWS_PROFILE:-default}

[ ! -d ${BUILD_PREFIX} ] && mkdir ${BUILD_PREFIX}

# Use docker to install packages into a target directory
docker run \
  --rm -ti \
  -v ${PWD}:/opt \
  -w /opt \
  python:${PYTHON_VERSION}-alpine \
  /bin/sh -c \
    "pip install -r requirements-${PYTHON_VERSION}.txt -t ${BUILD_PREFIX}"

# Add relevant code to build directory
cp -r \
  ./aws_lambda.py \
  ./slack_notification \
  ${BUILD_PREFIX}

rm -f ${PROJECT_NAME}.zip
find ./ -type f -name "*.pyc" -exec rm -f \{} \;
find ./ -type d -name "__pycache__" -exec rm -rf \{} \;

# Build zip package to be deployed to AWS
pushd ${BUILD_PREFIX} && zip -r ../${PROJECT_NAME}.zip ./ -x "*.pyc" "*.swa" "*.swp" && popd

aws lambda update-function-code \
  --profile ${AWS_PROFILE} \
  --function-name ${PROJECT_NAME} \
  --zip-file fileb://${PROJECT_NAME}.zip \
  --region ${AWS_REGION}

