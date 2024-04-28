from typing import Final


class JSONBotException(Exception):
    ...


class MissingConfig(JSONBotException):
    ...


class ImproperConfig(JSONBotException):
    ...


class ConfigValidationError(JSONBotException):
    ...


__all__: Final[tuple[str, ...]] = (
    "JSONBotException",
    "MissingConfig",
    "ImproperConfig",
    "ConfigValidationError",
)
