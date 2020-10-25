import yaml
import os


class Credentials():
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.public_channel = int(os.getenv('PUBLIC_CHANNEL'))
        self.private_channel = int(os.getenv('PRIVATE_CHANNEL'))


class Config():
    def __init__(self):
        self.persistent = False
        self.public_test = True
        self.interval = 10  # in minutes
        self.minutes_between_brackets = 30


credentials = Credentials()
config = Config()