import glob
from setuptools import setup, find_packages

setup(
    name="telegram-proverb",
    version="0.1.0",
    scripts=["./proverb_bot.py"],
    packages=find_packages(),
    package_data={"proverb_pro": ["backgrounds/*", "AmaticSC-Bold.ttf"]},
    install_requires=["pillow", "beautifulsoup4", "telepot"],
)
