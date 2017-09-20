import os
from bot import Bot

SLACK_BOT = Bot(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    name=os.environ.get('SLACK_BOT_NAME'),
    id=os.environ.get('SLACK_BOT_ID'),
)

WEB_SOCKET_POLL_DELAY = 1