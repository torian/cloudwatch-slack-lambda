# vim:ts=4:sw=4:et:ft=python

import os
import sys
import boto3
import logging
import json
import requests
import distutils.util

###############################################################################

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()

RUN_LOCAL = distutils.util.strtobool(os.environ.get('LOCAL', 'False'))

if RUN_LOCAL:
    SLACK_HOOK_URL = os.environ.get('SLACK_HOOK_URL')
else:
    from base64 import b64decode
    SLACK_HOOK_URL_ENC = os.environ.get('SLACK_HOOK_URL')
    SLACK_HOOK_URL     = boto3.client('kms').decrypt(
            CiphertextBlob = b64decode(SLACK_HOOK_URL_ENC)
        )['Plaintext']

# The Slack channel to send a message to stored in the slackChannel environment variable
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')

# Loggers config
logger = logging.getLogger()
logger.setLevel(getattr(logging, LOGLEVEL))

def main(event, context):

    logger.debug(json.dumps(event))

    message = event['Records'][0]['Sns']['Message']

    logger.debug(json.dumps(message))

    alarm_name = message['AlarmName']
    new_state  = message['NewStateValue']
    reason     = message['NewStateReason']
    old_state  = message['OldStateValue']
    trigger    = message['Trigger']

    logger.debug("[{}] {}".format(new_state, alarm_name))

    # Render the slack attachment
    slack_attachment = {
        "fallback": "{}".format(alarm_name),
        "pretext": "{}".format(alarm_name),
        "color": "{}".format("good" if new_state == "OK" else "danger"),
        "fields": [
            {
                "title": "Current Sate: {}".format(new_state),
                "value": "Trigger: {} {} {} {} for {} period/s of {} seconds".format(
                    trigger['Statistic'],
                    trigger['MetricName'],
                    trigger['ComparisonOperator'],
                    trigger['Threshold'],
                    trigger['EvaluationPeriods'],
                    trigger['Period']
                ),
                "short": True
            }
        ]
    }

    logger.debug(json.dumps(slack_attachment))

    slack_message = {
        "channel": SLACK_CHANNEL,
        "attachments": [ slack_attachment ]
    }

    payload_json = json.dumps(slack_message).encode('utf-8')

    r = requests.post(SLACK_HOOK_URL, data = payload_json)

    if r.status_code != 200:
        logger.error(
            "Status code: {} - {}". format(
                r.status_code,
                r.text
            )
        )
        sys.exit(1)

    logger.info("Notification sent to %s", slack_message['channel'])

    return True

