from __future__ import annotations

from typing import Final, Literal, NotRequired, TypedDict, Union

from discord import Member, TextChannel, Thread, User, VoiceChannel
from discord.abc import Messageable

type JSONConfigCommandArgument = Literal[
    "string",
    "integer",
    "float",
    "mention.user",
    "mention.member",
    "mention.channel.all",
    "mention.channel.text",
    "mention.channel.thread",
    "mention.channel.vc",
]

type DiscordCommandArgument = Union[
    str,
    int,
    float,
    User,
    Member,
    Messageable,
    TextChannel,
    Thread,
    VoiceChannel,
]


class JSONConfig(TypedDict):
    token: str
    commands: list[JSONCommand]


class JSONCommand(TypedDict):
    name: str
    desc: str
    args: list[JSONCommandArgument]
    resp: str


class JSONCommandArgument(TypedDict):
    name: str
    desc: str
    type: JSONConfigCommandArgument
    lt: NotRequired[int]
    gt: NotRequired[int]
    max_len: NotRequired[int]
    min_len: NotRequired[int]


__all__: Final[tuple[str, ...]] = (
    "JSONConfigCommandArgument",
    "JSONConfig",
    "JSONCommand",
    "JSONCommandArgument",
)
