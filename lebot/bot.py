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

    def check_output(self, output):
        return output \
               and output.get('type') == "message" \
               and not self.user.is_by_me(output.get('user'))

    def parse_slack_output(self, slack_rtm_output):
        output_list = slack_rtm_output

        if not output_list and len(output_list) <= 0:
            return None, None

        for output in output_list:
            if not self.check_output(output):
                continue

            text, channel = output.get('text'), output.get('channel')

            if self.user.is_mentioned(text=text):
                text = text.split(self.user.at)[1].strip().lower()

            return text, channel
        return None, None

    def run(self):
        if not self.helper.connect():
            print("Connection failed. Invalid Slack token or bot ID?")
            return

        print("StarterBot connected and running!")

        while True:
            command, channel = self.parse_slack_output(self.helper.read())

            if command and channel:
                self.handle_command(command, channel)

            time.sleep(self.config.get('WEB_SOCKET_POLL_DELAY'))
