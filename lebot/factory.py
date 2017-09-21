from slackclient import SlackClient
from cerebro import cerebro
import bot, config, helper as hlpr


def slack_bot():
    cfg = config.CONFIG

    slack_client = SlackClient(cfg.get('SLACK_BOT').token)

    helper = hlpr.SlackHelper(client=slack_client)

    return bot.SlackBot(
        config=config.CONFIG,
        helper=helper,
        cerebro=cerebro
    )