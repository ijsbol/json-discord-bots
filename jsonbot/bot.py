import re
from typing import Any, Final, Optional, Tuple
from discord import Client, Embed, Intents, Interaction, Object, app_commands
from discord.app_commands import Command

from jsonbot.types import JSONCommand, JSONConfig, DiscordCommandArgument


MY_GUILD: Final[Object] = Object(id=1044357852749365408)


class JSONBot(Client):
    def __init__(self, *, config: JSONConfig, intents: Intents):
        super().__init__(intents=intents)
        self._config = config
        self._commands: dict[str, JSONCommand] = {
            cmd['name']: cmd for cmd in self._config['commands']
        }
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        ...
        # self.tree.copy_global_to(guild=MY_GUILD)
        # await self.tree.sync(guild=MY_GUILD)

    def get_json_command(self, name: str) -> JSONCommand:
        return self._commands[name]


def _extract_variables(text) -> list[str]:
    pattern = r'\$\[(.*?)\]'
    return re.findall(pattern, text)


async def _get_variable_value(
    variable: str,
    json_command: JSONCommand,
    inter: Interaction[JSONBot],
) -> Any:
    variable_value = None
    if variable.startswith("inter"):
        variable_value = inter
        variable = variable.strip("inter")
        subsections = variable.split(".")[1::]
        for subsection in subsections:
            variable_value = getattr(variable_value, subsection)
    return variable_value


async def get_response(
    json_command: JSONCommand,
    inter: Interaction[JSONBot],
) -> Tuple[Optional[str], list[Embed]]:
    command_response = json_command['resp']
    variables = _extract_variables(command_response)
    for variable in variables:
        variable_full_format = f"$[{variable}]"
        variable_value = await _get_variable_value(
            variable=variable,
            json_command=json_command,
            inter=inter,
        )
        if variable_value is not None:
            command_response = command_response.replace(
                variable_full_format,
                str(variable_value),
            )
    return command_response, []


async def command_callback(
    inter: Interaction[JSONBot],
) -> None:
    assert inter.command is not None
    command_name = inter.command.qualified_name
    json_command = inter.client.get_json_command(command_name)
    response_content, embeds = await get_response(json_command, inter)
    await inter.response.send_message(
        content=response_content,
        embeds=embeds,
    )


def run(config: JSONConfig) -> None:
    bot = JSONBot(
        config=config,
        intents=Intents.none(),
    )
    for command in config['commands']:
        bot.tree.add_command(Command(
            name=command['name'],
            description=command['desc'],
            callback=command_callback,
        ))
    bot.run(config['token'])
