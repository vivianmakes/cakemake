import yaml
import os

class Credentials():
  def __init__(self):
    self.bot_token = os.getenv('BOT_TOKEN')
    self.broadcast_channel = int(os.getenv('BROADCAST_CHANNEL'))

credentials = Credentials()