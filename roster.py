import yaml
import random
import glob
import os
import imaging

class Player:
    def __init__(self):
        self.name = "Default"
        self.talent = 0
        self.luck = 0
        self.unluck = 0
        self.alignment = 0
        self.fame = 0
        self.icon = 'professor.png'
        self.pronoun = 'they'
        self.cheer = 0
        self.wins = 0
        self.losses = 0

        self.keywords = None

    def build_from_yaml(self, in_yaml):

        output = yaml.load(in_yaml, Loader=yaml.BaseLoader)

        self.name = output.get('name', "Default")
        self.talent = output.get('talent', random.randint(4, 8))
        self.luck = output.get('talent', random.randint(0, 8))
        self.unluck = output.get('talent', random.randint(0, 8))
        self.alignment = output.get('alignment', random.randint(-100, 100))
        self.fame = output.get('fame', 0)
        self.icon = output.get('icon', 'professor.png')
        self.pronoun = output.get('pronoun', 'they')
        self.wins = output.get('wins', 0)
        self.losses = output.get('losses', 0)

        self.keywords = output.get('keywords', {})

    def get_roll(self):
        roll = random.randint(0, self.talent+self.cheer)
        return roll

    def get_lucky(self):
        chance = random.randint(1,100)
        if chance < self.luck:
            return True
        else:
            return False

    def get_unlucky(self):
        chance = random.randint(1,100)
        if chance < self.unluck:
            return True
        else:
            return False

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

    def get_verb(self):
        if "adjectives" in self.keywords:
            return random.choice(self.keywords["adjectives"])
        else:
            return random.choice(['Whips up', 'Lovingly crafts', 'Assembles', 'Bakes', 'Fries up', 'Cooks up', 'Makes', 'Readies'])

    def get_portrait_path(self):
        return imaging.get_portrait_path(self.icon)

    def get_pronoun(self, conjugation):
        if conjugation == "their" or conjugation == "his" or conjugation == "her":
            if self.pronoun == 'he':
                return 'his'
            if self.pronoun == 'she':
                return 'her'
            if self.pronoun == 'they':
                return 'their'
        elif conjugation == "they" or conjugation == "she" or conjugation == "he":
            if self.pronoun == 'he':
                return 'he'
            if self.pronoun == 'she':
                return 'she'
            if self.pronoun == 'they':
                return 'they'
        elif conjugation == "them" or conjugation == "her" or conjugation == "him":
            if self.pronoun == 'he':
                return 'him'
            if self.pronoun == 'she':
                return 'her'
            if self.pronoun == 'they':
                return 'them'

# INIT ROSTER
players = []


def get_random_pair():
    p1 = random.choice(players)
    players_minus_p1 = players
    players_minus_p1.remove(p1)
    p2 = random.choice(players_minus_p1)

    return [p1, p2]


# LOAD ROSTER
for filename in glob.glob('players/*.yaml'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: #open file in readonly
        newplayer = Player()
        newplayer.build_from_yaml(f)
        players.append(newplayer)