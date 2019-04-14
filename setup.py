from setuptools import setup

setup(
    name="telegram-proverb",
    version="0.1.0",
    scripts=["./proverb_bot.py"],
    py_modules=["proverb_pro"],
    install_requires=["pillow", "beautifulsoup4", "telepot"],
)
