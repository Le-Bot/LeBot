import os
from entities import BotUser


CONFIG = {
    'SLACK_BOT': BotUser(
        token=os.environ.get('SLACK_BOT_TOKEN'),
        name=os.environ.get('SLACK_BOT_NAME'),
        id=os.environ.get('SLACK_BOT_ID'),
    ),
    'WEB_SOCKET_POLL_DELAY': 1
}