from slackclient import SlackClient

from common.slack import Slack

slack_token = 'xoxp-272417366868-272513196933-272490018914-1bc42af699d9720f9fd0ef2962bd7308'
sc = Slack.initialize(slack_token)

Slack.post_message("Testing, 1,2,3")

#Slack.post_enumerated_response_message("Testing 1,2,3", 3)


