from slackclient import SlackClient
from cerebro import cerebro
import bot, config, slack_helper


def slack_bot():
    cfg = config.CONFIG

    slack_client = SlackClient(cfg.get('SLACK_BOT').token)

    helper = slack_helper.SlackHelper(client=slack_client)

    return bot.SlackBot(
        config=config.CONFIG,
        helper=helper,
        cerebro=cerebro
    )