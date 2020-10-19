import yaml
import os

class Credentials():
  def __init__():
    self.bot_token = os.getenv('BOT_TOKEN')
    self.broadcast_channel = os.getenv('BROADCAST_CHANNEL')

credentials = Credentials()