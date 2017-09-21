import factory

if __name__ == '__main__':
    bot = factory.slack_bot(bot_type=factory.SLACK_RTM_BOT)
    bot.run()
