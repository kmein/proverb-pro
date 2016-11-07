#!/usr/bin/env python3
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from bs4 import BeautifulSoup
import os
import random
import urllib.request

PROVERB_GENERATOR = "http://sprichwort.gener.at/or/"

IMAGE_DIR = "img"
OUTPUT_DIR = "out"

FONT_FILE = "AmaticSC-Bold.ttf"
FONT_SCALE = 0.8


def get_proverb():
    with urllib.request.urlopen(PROVERB_GENERATOR) as f:
        html = f.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        proverb = soup.html.body.find(class_="spwort").string
        return proverb

def get_random_image():
    cwd = os.path.dirname(__file__)
    return os.path.join(cwd, IMAGE_DIR, random.choice(os.listdir(IMAGE_DIR)))

def apply_proverb(image_path, proverb):
    assert os.path.exists(FONT_FILE)

    def normalise(value):
        import string
        allowed = string.ascii_letters + string.digits
        return ''.join(c if c in allowed else '-' for c in value.lower())

    def get_main_color(image):
        width, height = image.size
        colors = image.getcolors(width * height)
        max_occurence, most_present = 0, 0
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        return most_present

    def complementary_colour(rgb):
        return tuple(255 - b for b in rgb)

    fontsize = 1 # starting font size
    image = Image.open(image_path)
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, fontsize)
    while font.getsize(proverb)[0] < FONT_SCALE * width: # increase font size until it fits the image
        fontsize += 1
        font = ImageFont.truetype(FONT_FILE, fontsize)

    w, h = font.getsize(proverb)
    coord = ((width - w)/2, (height - h)/2)

    colour = complementary_colour(get_main_color(image))

    draw.text(coord, proverb, colour, font=font)

    path = os.path.join(OUTPUT_DIR, normalise(proverb) + ".jpg")
    print(path)
    image.save(path)

if __name__ == "__main__":
    apply_proverb(get_random_image(), get_proverb())

