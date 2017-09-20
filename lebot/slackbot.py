import time
from slackclient import SlackClient
from config import *


def post_message(response, channel):
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def handle_command(command, channel):
    response = command + " back at you!"
    post_message(response=response, channel=channel)


def get_bot_id():
    api_call = slack_client.api_call("users.list")

    if not api_call.get('ok'):
        print("could not find bot user with the name " + SLACK_BOT.name)

    users = api_call.get('members')
    for user in users:
        if 'name' in user and user.get('name') == SLACK_BOT.name:
            print("Bot ID for '" + user['name'] + "' is " + user.get('id'))


def check_output(output):
    return output \
        and output.get('type') == "message" \
        and not SLACK_BOT.is_by_me(output.get('user'))


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if not output_list and len(output_list) <= 0:
        return None, None

    for output in output_list:
        if not check_output(output):
            continue

        text, channel = output.get('text'), output.get('channel')

        if SLACK_BOT.is_mentioned(text=text):
            text = text.split(SLACK_BOT.at)[1].strip().lower()

        return text, channel
    return None, None


def run():
    if not slack_client.rtm_connect():
        print("Connection failed. Invalid Slack token or bot ID?")
        return

    print("StarterBot connected and running!")

    while True:
        command, channel = parse_slack_output(slack_client.rtm_read())

        if command and channel:
            handle_command(command, channel)

        time.sleep(WEB_SOCKET_POLL_DELAY)


if __name__ == "__main__":
    slack_client = SlackClient(SLACK_BOT.token)
    run()
