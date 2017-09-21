class SlackHelper(object):
    def __init__(self, client):
        self.client = client

    def post_message(self, text, channel):
        return self.client.api_call("chat.postMessage", channel=channel, text=text, as_user=True)

    def get_users(self):
        api_call = self.client.api_call("users.list")

        if not api_call.get('ok'):
            return []

        return api_call.get('members')

    def connect(self):
        return self.client.rtm_connect()

    def read(self):
        return self.client.rtm_read()