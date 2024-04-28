from sys import argv

from jsonbot.errors import MissingConfig
from jsonbot.functions import load_config
from jsonbot.bot import run


if not len(argv) >= 2:
    raise MissingConfig(
        "Missing json bot file location, please run this with:"
        " 'python -m jsonbot path/to/bot.json'"
    )

file_location = argv[1]

config = load_config(file_location)

run(config)
