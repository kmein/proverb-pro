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

def weighted_average(items):
    item_count = sum(item[0] for item in items)
    item_sum = [0] * len(items[0][1])
    for freq, item in items:
        for i in range(len(item)):
            item_sum[i] += freq * item[i]
    return (isum // item_count for isum in item_sum)

def average_colour(image):
    width, height = image.size
    colours = image.getcolors(width * height)
    return weighted_average(colours)

def most_frequent_colour(image):
    width, height = image.size
    colours = image.getcolors(width * height)
    max_occurrence, most_present = 0, 0
    for c in colours:
        if c[0] > max_occurrence:
            max_occurrence, most_present = c
    return most_present

def black_white(image):
    red, green, blue = average_colour(image)
    return (0, 0, 0) if (red + green + blue) / 3 > 127 else (255, 255, 255)

def complementary(rgb):
    return tuple(255 - b for b in rgb)


def apply_proverb(image_path, proverb, main_colour=black_white):
    assert os.path.exists(FONT_FILE)
    assert os.path.exists(image_path)

    def normalise(value):
        import string
        allowed = string.ascii_letters + string.digits
        return ''.join(
            c if c in allowed else '-'
            for c in value.lower()
                          .replace(".", "")
                          .replace(",", "")
                          .replace("ß", "ss")
                          .replace("ö", "oe")
                          .replace("ü", "ue")
                          .replace("ä", "ae"))

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

    colour = main_colour(image)

    draw.text(coord, proverb, colour, font=font)

    path = os.path.join(OUTPUT_DIR, normalise(proverb) + ".jpg")
    image.save(path)
    return path

if __name__ == "__main__":
    from argparse import ArgumentParser

    AVERAGE_CR = "average"
    FREQUENCY_CR = "frequency"
    BLACKWHITE_CR = "blackwhite"

    parser = ArgumentParser(description="Generate hilarious proverbs on top of inspiring pictures")
    parser.add_argument("-i", "--image", help="image file path", nargs="?")
    parser.add_argument("-t", "--text", help="text to add", nargs="?")
    parser.add_argument("-c", "--colours", help="select the colour recognition mechanism",
            choices=[AVERAGE_CR, FREQUENCY_CR, BLACKWHITE_CR], default=BLACKWHITE_CR, nargs="?")
    args = parser.parse_args()

    text = get_proverb() if args.text is None else args.text
    image = get_random_image() if args.image is None else args.image
    if args.colours == AVERAGE_CR:
        colour_recognition = lambda x: complementary(average_colour(x))
    elif args.colours == FREQUENCY_CR:
        colour_recognition = lambda x: complementary(most_frequent_colour(x))
    elif args.colours == BLACKWHITE_CR:
        colour_recognition = black_white

    print(apply_proverb(image, text, colour_recognition))

