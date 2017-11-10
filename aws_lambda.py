
import logging

from slack_notification.main import main

logger = logging.getLogger('lambda_handler')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    main(event, context)

# vim:ts=4:sw=4:et:ft=python
