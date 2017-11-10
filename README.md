# Cloudwatch Alarms to Slack

AWS Lambda function to send CloudWatch alarms to a slack channel through
a Slack `Incomming webhook`.

## Environment variables

  * `SLACK_CHANNEL`: Slack channel where to send messages
  * `SLACK_HOOK_URL`: Incomming webhook url. This value should be 
    encrypted with `KMS` when the function is deployed on AWS
  * `LOGLEVEL`: (default: `INFO`)
  * `LOCAL`: (default: `False`) Run the function locally. Used for testing

## Testing locally

One option is to use `python-lambda-local`, which can be installed through `pip`.

Export the variable `LOCAL=False`, and the related slack vars. Then, run:

```
$> python-lambda-local \
  -f lambda_handler \
  -l slack_notification \
  -t 5 \
  aws_lambda.py tests/events/sns.event-alarm.json
```

## Deploying

Make sure to have a lambda function created wit the name of this repo, and that
you export the following variables:

  * `AWS_REGION`
  * `AWS_PROFILE`

```
$> ./build.sh

```

