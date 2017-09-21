import time


class SlackBot(object):
    def __init__(self, config, helper, cerebro):
        self.config = config
        self.helper = helper
        self.cerebro = cerebro
        self.user = config.get('SLACK_BOT')

    def handle_command(self, command, channel):
        response = self.cerebro.run([command, ])
        print('Command: "{}"   Response: "{}"'.format(command, response))
        self.helper.post_message(text=response, channel=channel)

    def get_bot_id(self):
        users = self.helper.get_users()
        for user in users:
            if 'name' in user and user.get('name') == self.user.name:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                self.user.id = user.get('id')

    def validate(self, event):
        return event \
               and event.get('type') == "message" \
               and not self.user.is_by_me(event.get('user'))

    def parse_input_event(self, event):
        if not self.validate(event):
            return None, None

        text, channel = event.get('text'), event.get('channel')

        if self.user.is_mentioned(text=text):
            text = text.split(self.user.at)[1].strip().lower()

        return text, channel


class SlackRTMBot(SlackBot):

    def parse_rtm_message(self, rtm_message):
        event_list = rtm_message

        if not event_list and len(event_list) <= 0:
            return None, None

        for event in event_list:
            text, channel = self.parse_input_event(event=event)

            if text and channel:
                return text, channel

        return None, None

    def run(self):
        if not self.helper.connect():
            print("Connection failed. Invalid Slack token or bot ID?")
            return

        print("StarterBot connected and running!")

        while True:
            command, channel = self.parse_rtm_message(self.helper.read())

            if command and channel:
                self.handle_command(command, channel)

            time.sleep(self.config.get('WEB_SOCKET_POLL_DELAY'))


class SlackEventBot(SlackBot):
    def execute(self, event, token):
        if not self.user.token_verification(token=token):
            return "Invalid Slack verification token: ", 403, {"X-Slack-No-Retry": 1}

        if event:
            command, channel = self.parse_input_event(event=event)

            if command and channel:
                self.handle_command(command, channel)

            return "Success", 200, {"X-Slack-No-Retry": 1}

        return "Invalid Event", 404, {"X-Slack-No-Retry": 1}
