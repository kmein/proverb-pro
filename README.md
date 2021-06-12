# The Proverb Pro

Welcome to the precious playful Proverb Pro, a program
that generates completely useless German proverbs using
[Sprichwortgenerator](http://sprichwort.gener.at/or/) and throws it together
with an inspirational picture in the background.

## Setup

Run `pip3 install -r requirements.txt` and you should be up and running, not
only for the Proverb Pro, but also for the Proverb Bot.

## Usage

```
usage: proverb_pro.py [-h] [-i [IMAGE]] [-t [TEXT]]
                      [-c [{average,frequency,blackwhite}]]

Generate hilarious proverbs on top of inspiring pictures

optional arguments:
  -h, --help            show this help message and exit
  -i [IMAGE], --image [IMAGE]
                        image file path
  -t [TEXT], --text [TEXT]
                        text to add
  -c [{average,frequency,blackwhite}], --colours [{average,frequency,blackwhite}]
                        select the colour recognition mechanism
```

If any of `-i` and `-t` are not provided, they are going to be randomly chosen:
The image is taken from the `img/` directory within this repo and the text comes
from [Sprichwortgenerator](http://sprichwort.gener.at/or/).

If `-c` is not used, `blackwhite` will be chosen. `average` colours the text
based on the average colour of the image, `frequency` uses the most frequent
colour and `blackwhite` uses the average colour and then either uses black or
white as the text colour.

When `proverb_pro.py` is run, it outputs the path of the generated image file.
**NOTE**: By default it outputs to a folder called `out/` which isn't present in
this repo because stupid git can't handle empty directories.

## Setup

For using the Proverb Bot, you need a Telegram bot token for Proverb
Bot to use.  You can obtain them by sending `/newbot` to the
["BotFather"](https://telegram.me/botfather).

Once you have the token, save it into a file called `proverb_bot.token`.

## Usage

The bot program is an endlessly looping program, so you just run
`./proverb_bot.py` either with nohup or in a terminal session you don't need,
lay back and enjoy the weird proverbs.
**NOTE**: Some of the pictures are quite large, so generating and sending may
take a while, especially on older (or cheaper) hardware.
