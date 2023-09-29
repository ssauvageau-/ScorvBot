import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import numpy as np
import matplotlib.pyplot as plt


@app_commands.guild_only()
class GraphRoleCommandGroup(app_commands.Group, name="graph-roles"):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.bot = bot
        super().__init__()

    @app_commands.command(name="mastery")
    async def graph_roles(self, interaction: discord.Interaction):
        role_list = interaction.guild.roles
        masteries = [
            "Soldier",
            "Demolitionist",
            "Occultist",
            "Nightblade",
            "Arcanist",
            "Shaman",
            "Inquisitor",
            "Necromancer",
            "Oathkeeper",
        ]
        pruned_roles = [role for role in role_list if role.name in masteries]
        pruned_roles.reverse()
        usage = [len(role.members) for role in pruned_roles]

        ypos = np.arange(len(masteries))
        plt.bar(
            ypos,
            usage,
            color=[
                "yellow",
                "orange",
                "pink",
                "teal",
                "green",
                "cyan",
                "purple",
                "turquoise",
                "peru",
            ],
        )
        plt.xticks(ypos, masteries, rotation=45, ha="right")
        plt.tight_layout()

        filename = "role_output.png"
        plt.savefig(fname=filename)
        await interaction.response.send_message(file=discord.File(filename))
        os.unlink(filename)

    # TODO - Add graph function for Server Ping notifs? Or don't. Idk.
