#!/usr/bin/env python3
from PIL import Image, ImageColor, ImageDraw, ImageFont
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
    assert os.path.exists(image_path)

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

    def adjust_font_size(image_width, proverb):
        fontsize = 1
        font = ImageFont.truetype(FONT_FILE, fontsize)
        while font.getsize(proverb)[0] < FONT_SCALE * image_width:
            fontsize += 1
            font = ImageFont.truetype(FONT_FILE, fontsize)
        return font

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    font = adjust_font_size(width, proverb)
    w, h = font.getsize(proverb)

    coord = ((width - w)/2, (height - h)/2)

    colour = complementary_colour(get_main_color(image))

    draw.text(coord, proverb, colour, font=font)

    path = os.path.join(OUTPUT_DIR, normalise(proverb) + ".jpg")
    print(path)
    image.save(path)

if __name__ == "__main__":
    apply_proverb(get_random_image(), get_proverb())

