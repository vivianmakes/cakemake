from PIL import Image
import os
from io import BytesIO
import discord
import io

def get_portrait_path(filename):
    portrait_path = os.path.join('portraits', filename)
    image_path = os.path.join(os.getcwd(), portrait_path)

    return image_path


def concatenate(filename1, filename2):
    im1 = Image.open(filename1)
    im2 = Image.open(filename2)

    product = Image.new('RGB', (im1.width + im2.width, im1.height))
    product.paste(im1, (0, 0))
    product.paste(im2, (im1.width, 0))

    return product


def open_image_path(image_path):
    im = Image.open(image_path)
    return im


def get_image_file(image_object):
    with BytesIO() as image_binary:
        image_object.save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='image.png')