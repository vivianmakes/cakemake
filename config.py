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
        self.public_test = False
        self.interval = 1  # in minutes


credentials = Credentials()
config = Config()