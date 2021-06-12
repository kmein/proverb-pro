from proverb_pro import (
    get_proverb,
    get_random_image,
    apply_proverb,
    complementary,
    average_colour,
    most_frequent_colour,
    black_white,
)
from argparse import ArgumentParser


def run():
    AVERAGE_CR = "average"
    FREQUENCY_CR = "frequency"
    BLACKWHITE_CR = "blackwhite"

    parser = ArgumentParser(
        description="Generate hilarious proverbs on top of inspiring pictures"
    )
    parser.add_argument("-i", "--image", help="image file path", nargs="?")
    parser.add_argument("-t", "--text", help="text to add", nargs="?")
    parser.add_argument(
        "-c",
        "--colours",
        help="select the colour recognition mechanism",
        choices=[AVERAGE_CR, FREQUENCY_CR, BLACKWHITE_CR],
        default=BLACKWHITE_CR,
        nargs="?",
    )
    args = parser.parse_args()

    text = get_proverb() if args.text is None else args.text
    image = get_random_image() if args.image is None else args.image

    def colour_recognition(x):
        if args.colours == AVERAGE_CR:
            return complementary(average_colour(x))
        elif args.colours == FREQUENCY_CR:
            return complementary(most_frequent_colour(x))
        elif args.colours == BLACKWHITE_CR:
            return black_white(x)

    print(apply_proverb(image, text, colour_recognition))
