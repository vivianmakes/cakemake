import yaml
import random
import glob
import os

class Player:
    def __init__(self):
        self.name = "Default"
        self.talent = 0
        self.alignment = 0
        self.fame = 0

        self.keywords = None

    def build_from_yaml(self, in_yaml):

        output = yaml.load(in_yaml, Loader=yaml.CLoader)

        self.name = output.get('name', "Default")
        self.talent = output.get('talent', 0)
        self.alignment = output.get('alignment', 0)
        self.fame = output.get('fame', 0)

        self.keywords = output.get('keywords', None)

    def bake(self):
        # Called to bake a cake.
        return

    def get_sound(self):
        if "sounds" in self.keywords:
            return random.choice(self.keywords["sounds"])
        else:
            return random.choice(['BIFF!', 'POW!', 'ZOT!', 'KAPOW!', 'WOAH!', 'SLORP!'])

    def get_cake_type(self):
        if "cakes" in self.keywords:
            return random.choice(self.keywords["cakes"])
        else:
            return random.choice(['Wedding Cake', 'Bunt Cake', 'Layer Cake', 'Birthday Cake', 'Pound Cake', 'Fruit Pie', 'Ice Cream Cake', 'Tart'])

    def get_cake_flavor(self):
        if "flavors" in self.keywords:
            return random.choice(self.keywords["flavors"])
        else:
            return random.choice(['Chocolate', 'Strawberry', 'Lemon', 'Fudge', 'Apple', 'Pumpkin', 'Vanilla', 'Orange'])

    def get_cake_adjective(self):
        if "adjectives" in self.keywords:
            return random.choice(self.keywords["adjectives"])
        else:
            return random.choice(['Juicy', 'Delicious', 'Spicy', 'Beautiful', 'Small', 'Huge', 'Creamy', 'Tangy'])


# INIT ROSTER
players = []

# LOAD ROSTER
for filename in glob.glob('players/*.yaml'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: #open file in readonly
        newplayer = Player()
        newplayer.build_from_yaml(f)
        players.append(newplayer)