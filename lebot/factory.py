from slackclient import SlackClient
from cerebro import cerebro
import bot, config, helper as hlpr

SLACK_EVENT_BOT = 1
SLACK_RTM_BOT = 2


def slack_bot(bot_type):
    cfg = config.CONFIG

    slack_client = SlackClient(cfg.get('SLACK_BOT').token)

    helper = hlpr.SlackHelper(client=slack_client)

    if bot_type == SLACK_EVENT_BOT:
        return bot.SlackEventBot(config=config.CONFIG, helper=helper, cerebro=cerebro)
    else:
        return bot.SlackRTMBot(config=config.CONFIG, helper=helper, cerebro=cerebro)