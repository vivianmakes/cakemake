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

    product = Image.new('RGBA', (im1.width + im2.width, im1.height))
    product.paste(im1, (0, 0))
    product.paste(im2, (im1.width, 0))

    return product


def concatenate_multiple(*filenames):
    images = []
    for iter in range(len(filenames)):
        images.append(Image.open(filenames[iter]))

    height = 0
    width = 0
    for image in images:
        height = max(height, image.height)
        width += image.width

    product = Image.new('RGBA', (width, height))

    cursorx = 0
    for image in images:
        product.paste(image, (cursorx, 0))
        cursorx += image.width

    return product


def open_image_path(image_path):
    im = Image.open(image_path)
    return im


def get_image_file(image_object):
    with BytesIO() as image_binary:
        image_object.save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='image.png')


def get_vs_graphic(impath1, impath2):
    return concatenate_multiple(impath1, "images/vs.png", impath2)


def get_win_graphic(result):
    # IN: A result.
    pimages = []
    ppaths = [result.p1.get_portrait_path(), "images/spacer.png", result.p2.get_portrait_path()]
    for path in ppaths:
        pimages.append(Image.open(path))

    p1_judge_images = []
    for judgy in result.p1_details.judges:
        p1_judge_images.append(Image.open(judgy.get_portrait_path()))
    p2_judge_images = []
    for judgy in result.p2_details.judges:
        p2_judge_images.append(Image.open(judgy.get_portrait_path()))

    height = 0
    width = 0
    for image in pimages:
        height = max(height, image.height)
        width += image.width
    height += 55

    product = Image.new('RGBA', (width, height))

    cursorx = 0
    for pimage in pimages:
        product.paste(pimage, (cursorx, 0))
        cursorx += pimage.width

    cursorx=0
    for jimage in p1_judge_images:
        resized = jimage.resize((48, 48), Image.ANTIALIAS)
        product.paste(resized, (cursorx, height-50))
        cursorx += resized.width + 3

    cursorx = 48
    for jimage in p2_judge_images:
        resized = jimage.resize((48, 48), Image.ANTIALIAS)
        product.paste(resized, (width-cursorx, height - 50))
        cursorx += resized.width + 3

    cursorx = 0
    if result.winner is result.p2:
        cursorx = width-150
    foreground = Image.open("images/outline.png")
    product.paste(foreground, (cursorx, 0), foreground)

    return product


def get_roster_graphic(path_list):
    images = []
    tile_size = 64
    for iter in path_list:
        img = Image.open(iter)
        img = img.resize((tile_size, tile_size), Image.ANTIALIAS)
        images.append(img)

    product = Image.new('RGBA', (384, 64))
    bg = Image.open('images/roster_back.png')
    product.paste(bg, (0, 0))

    cursorx = 0
    for image in images:
        product.paste(image, (cursorx, 0))
        cursorx += 64

    return product
