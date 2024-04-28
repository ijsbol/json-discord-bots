
import json
import os

from dotenv import load_dotenv

from jsonbot.constants import MAXIMUM_ARGUMENTS
from jsonbot.errors import ConfigValidationError, ImproperConfig, MissingConfig
from jsonbot.types import JSONCommandArgument, JSONConfig


load_dotenv()


def _validatae_command_argument(argument: JSONCommandArgument) -> None:
    raise NotImplemented()


def _validate_config(config: JSONConfig) -> JSONConfig:
    assert config["token"] is not None
    assert len(config["token"]) > 0
    token: str = config["token"]
    if token.startswith(".env"):
        config["token"] = str(os.getenv(token.split("/")[1]))
    existing_commands: list[str] = []
    for command in config["commands"]:
        if command["name"].lower() in existing_commands:
            raise ConfigValidationError(
                f"Duplicate command defined: {command["name"]}",
            )
        if len(command["args"]) > MAXIMUM_ARGUMENTS:
            raise ConfigValidationError(
                f"Command '/{command["name"]}' has {len(command['args'])} arguments,"
                f" the maximum is {MAXIMUM_ARGUMENTS}."
            )

        # for argument in command["args"]:
        #     _validatae_command_argument(argument)
    return config


def load_config(file_location: str) -> JSONConfig:
    if not os.path.exists(file_location):
        raise MissingConfig(
            "Your config file cannot be found at the specified location: "
            + f"'{file_location}'"
        )

    with open(file_location, "r") as f:
        config: JSONConfig = json.loads(f.read())

    try:
        config = _validate_config(config)
    except AssertionError or KeyError or ConfigValidationError as e:
        raise ImproperConfig(
            f"Your config file is improperly formatted: {e}",
        )

    return config
