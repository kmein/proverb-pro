from PIL import Image, ImageColor, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import os
import random
import tempfile
import urllib.request
import importlib.resources

import proverb_pro.assets
import proverb_pro.assets.backgrounds

PROVERB_GENERATOR = "http://sprichwort.gener.at/or/"

FONT_SCALE = 0.8


def get_proverb():
    with urllib.request.urlopen(PROVERB_GENERATOR) as f:
        html = f.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        proverb = soup.html.body.find(class_="spwort").string
        return proverb


def get_random_image():
    background_images = importlib.resources.contents(proverb_pro.assets.backgrounds)
    return importlib.resources.path(
        proverb_pro.assets.backgrounds, random.choice(list(background_images))
    )


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
    def normalise(value):
        import string

        allowed = string.ascii_letters + string.digits
        return "".join(
            c if c in allowed else "-"
            for c in value.lower()
            .replace(".", "")
            .replace(",", "")
            .replace("ß", "ss")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ä", "ae")
        )

    def adjust_font_size(image_width, proverb):
        with importlib.resources.path(
            proverb_pro.assets, "AmaticSC-Bold.ttf"
        ) as font_file:
            fontsize = 1
            font = ImageFont.truetype(str(font_file), fontsize)
            while font.getsize(proverb)[0] < FONT_SCALE * image_width:
                fontsize += 1
                font = ImageFont.truetype(str(font_file), fontsize)
            return font

    with image_path as path:
        image = Image.open(str(path))
        draw = ImageDraw.Draw(image)
        width, height = image.size
        font = adjust_font_size(width, proverb)
        w, h = font.getsize(proverb)

        coord = ((width - w) / 2, (height - h) / 2)

        colour = main_colour(image)

        draw.text(coord, proverb, colour, font=font)

        path = normalise(proverb) + ".jpg"
        image.save(path)
        return path
