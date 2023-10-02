import base64
import os
import json
from typing import Dict
import datetime as dt
import random

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


@app_commands.guild_only()
class RaffleCommandGroup(app_commands.Group, name="raffle"):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.bot = bot
        self.raffle_json_path = os.getenv("RAFFLE_JSON_PATH")
        self.raffle_config = os.getenv("RAFFLE_CONFIG_NAME")
        try:
            self.raffle_dict = self.load_raffle()
        except json.decoder.JSONDecodeError:
            self.raffle_dict = {}
        except FileNotFoundError:
            self.raffle_dict = {}
            if not os.path.exists("json"):
                os.makedirs("json")
            os.close(os.open(self.raffle_json_path, os.O_CREAT))
        super().__init__()

    def load_raffle(self) -> Dict[str, Dict]:
        with open(self.raffle_json_path, "r", encoding="utf-8") as disk_lib:
            return json.loads(disk_lib.read())

    def dump_raffle(self) -> None:
        with open(self.raffle_json_path, "w", encoding="utf-8") as disk_lib:
            disk_lib.write(json.dumps(self.raffle_dict, sort_keys=True))

    # Don't really know how we'd want to use these
    def encode_raffle_data(self, data: str) -> str:
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")

    def decode_raffle_data(self, data: str) -> str:
        return base64.b64decode(data.encode("utf-8")).decode("utf-8")

    @app_commands.command(
        name="join", description="Join an upcoming raffle for fabulous prizes!"
    )
    async def join_raffle(self, interaction: discord.Interaction):
        member = interaction.user
        if not self.raffle_dict:
            await interaction.response.send_message(
                f"Sorry, {interaction.user.global_name}, but there does not appear to be an active raffle!",
                ephemeral=True,
            )
            return
        if member.name in self.raffle_dict:
            self.raffle_dict[member.name]["submissions"] += 1
            self.dump_raffle()
            await interaction.response.send_message(
                "Your submission has been recorded!", ephemeral=True
            )
            return
        currtime = dt.datetime.now(tz=dt.timezone.utc)
        diff = currtime - member.joined_at
        diff_s = diff.total_seconds()
        days = divmod(diff_s, 86400)  # 86400 seconds in a day
        if days[0] < int(self.raffle_dict[self.raffle_config]["age"]):
            await interaction.response.send_message(
                f"Sorry, {interaction.user.global_name}, but your Discord account is not old enough to enter this raffle!"
            )
            self.raffle_dict[self.raffle_config]["youth"] += 1
            self.dump_raffle()
            return
        if member.bot:
            await interaction.response.send_message("No bots allowed!", ephemeral=True)
        # OTHERWISE
        self.raffle_dict[member.name] = {
            "id": member.id,
            "submissions": 1,
            "entry": str(currtime),
            "hasWon": False,
        }
        self.dump_raffle()
        await interaction.response.send_message(
            f"{interaction.user.global_name}, you have entered yourself into the {self.raffle_dict[self.raffle_config]['name']} raffle! Good luck!",
            ephemeral=True,
        )

    @app_commands.command(name="create", description="Create a raffle.")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def create_raffle(
        self,
        interaction: discord.Interaction,
        account_age: str,
        allow_multiple_wins: str,
        name: str,
    ):
        if self.raffle_dict:
            await interaction.response.send_message(
                f"Sorry, {interaction.user}, a raffle is already ongoing!"
            )
            return
        self.raffle_dict[self.raffle_config] = {
            "age": account_age,
            "name": name,
            "multiple": allow_multiple_wins.lower() in ("true", "yes", "1", "y", "t"),
            "youth": 0,
        }
        self.dump_raffle()
        await interaction.response.send_message(f"Raffle {name} created.")

    @app_commands.command(name="close", description="Close an active raffle.")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def close_raffle(self, interaction: discord.Interaction):
        # Don't need to bother checking if there is a raffle...
        self.raffle_dict = {}
        self.dump_raffle()
        await interaction.response.send_message("Raffle closed successfully.")
        await interaction.message.delete()

    @app_commands.command(name="pull", description="Pull a winner from the raffle!")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def pull_raffle(self, interaction: discord.Interaction):
        """
        So, if we don't want people to be able to win multiple times, we will set their win-tracker to True if they've won.
        This will keep the while loop going on subsequent pulls.
        If we don't care, we'll never set their win-tracker to True, and therefore the if statement in the while loop will never trigger.
        """
        lucky = False
        while not lucky:
            lucky = random.choice(list(self.raffle_dict.keys()))
            if lucky == self.raffle_config:
                lucky = ""
                continue
            if self.raffle_dict[lucky]["hasWon"]:
                lucky = False
        await interaction.response.send_message(
            f"<@{self.raffle_dict[lucky]['id']}>, congratulations! You have won a FABULOUS prize! A moderator will contact you shortly with information about your reward."
        )
        if not self.raffle_dict[self.raffle_config]["multiple"]:
            self.raffle_dict[lucky]["hasWon"] = True
            self.dump_raffle()
        return

    @app_commands.command(name="meme", description="Haha funny")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def meme_embed(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.create_embed(interaction))

    def create_embed(self, interaction: discord.Interaction):
        raffle_embed = discord.Embed(
            title="Important Raffle Statistics", type="rich", color=0x00FFFF
        )
        raffle_embed.set_author(
            name=interaction.user, icon_url=interaction.user.avatar.url
        )
        spamCount = 0
        highest = (0, "")
        for entry in self.raffle_dict:
            if entry == self.raffle_config:
                continue
            subCount = self.raffle_dict[entry]["submissions"]
            if subCount > 1:
                spamCount += 1
                if subCount > highest[0]:
                    highest = (subCount, entry)
        raffle_embed.add_field(
            name="People that tried to abuse the system:", value=spamCount, inline=False
        )
        if spamCount > 0:
            raffle_embed.add_field(
                name="Biggest tryhard:",
                value=f"{highest[1]} at {highest[0]} extraneous resubmissions.",
                inline=False,
            )
        raffle_embed.add_field(
            name="Attempted Underage Gamblers:",
            value=self.raffle_dict[self.raffle_config]["youth"],
        )

        return raffle_embed
