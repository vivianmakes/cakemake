from PIL import Image
import os
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


def image_to_byte_array(image:Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr