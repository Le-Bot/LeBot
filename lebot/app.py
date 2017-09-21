import json

from flask import Flask, request, make_response, render_template

import factory

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    bot = factory.slack_bot(bot_type=factory.SLACK_EVENT_BOT)
    return make_response(bot.execute(event=slack_event.get('event'), token=slack_event.get('token')))


if __name__ == '__main__':
    app.run(debug=True)
