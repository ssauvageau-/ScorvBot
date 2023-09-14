import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from enums.mastery_roles import MasteryRoles


@app_commands.guild_only()
class AssignRoleCommandGroup(app_commands.Group, name="assign-role"):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.bot = bot
        super().__init__()

    @app_commands.command(
        name="mastery", description="Represent your favorite mastery!"
    )
    @app_commands.describe(mastery="The mastery role you want")
    async def assign_mastery_role(
        self, interaction: discord.Interaction, mastery: MasteryRoles
    ):
        user = interaction.user
        mastery_role_id = int(os.getenv(mastery.value))

        # Check if the user already has the role that they're asking for
        mastery_role = user.get_role(mastery_role_id)
        if mastery_role is not None:
            await user.remove_roles(
                mastery_role, reason="Unassigning existing master role"
            )
            await interaction.response.send_message(
                f"Unassigned the {mastery.name} role!", ephemeral=True
            )
            return

        # If the user already has a mastery role remove it
        for item in MasteryRoles:
            role_id = int(os.getenv(item.value))
            role = user.get_role(role_id)
            if role is not None:
                await user.remove_roles(role, reason="Removing existing master role(s)")

        # Assign new mastery role to user
        mastery_role = interaction.guild.get_role(mastery_role_id)
        await user.add_roles(mastery_role, reason="Assigning new mastery role")

        await interaction.response.send_message(
            f"Assigned the {mastery.name} role!", ephemeral=True
        )
