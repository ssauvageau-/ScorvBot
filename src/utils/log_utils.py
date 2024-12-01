import json
from typing import Union

import discord
from discord import app_commands


def format_user(user: discord.User) -> str:
    user_obj = {"name": user.name, "display_name": user.display_name, "id": user.id}
    return json.dumps(user_obj)


def format_app_command_name(command: app_commands.Command) -> str:
    output_arr = ["`", "/"]
    parent_commands = []
    parent = command.parent
    while parent is not None:
        parent_commands.extend([" ", parent.name])
        parent = parent.parent
    output_arr.extend(parent_commands[::-1])
    output_arr.extend([command.name, "`"])
    return "".join(output_arr)


def format_channel_name(
    channel: Union[discord.TextChannel, discord.ForumChannel, discord.Thread]
) -> str:
    if type(channel) == discord.Thread:
        return f"thread '{channel.name}' in #{channel.parent.name}"

    return f"#{channel.name}"
