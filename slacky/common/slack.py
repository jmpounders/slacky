from slackclient import SlackClient

class Slack():
    token = None
    client = None
    post_channel = '#dsi-ec-instructors'

    @staticmethod
    def initialize(token):
        Slack.token = token
        Slack.client = SlackClient(Slack.token)
        return Slack.client

    @staticmethod
    def post_message(title, message):
        result = Slack.client.api_call(
            "chat.postMessage",
            channel = Slack.post_channel,
            attachments = [{"title": title,
                            "text": message}]
        )
        return result

    @staticmethod
    def post_enumerated_response_message(title, message, num_opts):
        result = Slack.client.api_call(
            "chat.postMessage",
            channel = Slack.post_channel,
            attachments = [{"title": title,
                            "text": message}]
        )

        msg_ts = result['message']['ts']
        msg_channel = result['channel']

        emoji  = {1: "one",
                  2: "two",
                  3: "three",
                  4: "four",
                  5: "five",
                  6: "six",
                  7: "seven",
                  8: "eight",
                  9: "nine"}

        for i in range(num_opts):
            result = Slack.client.api_call(
                "reactions.add",
                name = emoji[i+1],
                channel = msg_channel,
                timestamp = msg_ts
            )

    @staticmethod
    def get_responses(channel, timestamp):
        result = Slack.client.api_call(
            "reactions.get",
            channel=channel,
            timestamp=timestamp
        )
        return result['message']['reactions']
