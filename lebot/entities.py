class BotUser(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.token = kwargs.get('token')
        self.at = '<@{user}>'.format(user=self.id)

    def is_me(self, name):
        return self.name == name

    def is_mentioned(self, text):
        return self.at in text

    def is_by_me(self, id):
        return self.id == id
