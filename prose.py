import os
import yaml
from random import choice


def random(filename):
    in_path = os.path.join("prose", filename)
    with open(os.path.join(os.getcwd(), in_path), 'r') as f:
        content = yaml.load(f, Loader=yaml.BaseLoader)
    output = choice(content)

    return output


def replace(input, find, replace):
    return input.replace(find, replace)