import json
from typing import Dict
import datetime as dt
import random

import discord
import redis.asyncio as redis
from discord import app_commands
from discord.ext import commands


RAFFLE_CONFIG_KEY = "raffle_config"
RAFFLE_SUBMISSIONS_KEY = "raffle_submissions"


@app_commands.guild_only()
class RaffleCommandGroup(app_commands.Group, name="raffle"):
    def __init__(self, bot: commands.Bot, redis_client: redis.Redis):
        self.bot = bot
        self.redis_client = redis_client
        super().__init__()

    @app_commands.command(
        name="count", description="Replies with the number of people in the raffle."
    )
    async def raffle_count(self, interaction: discord.Interaction):
        if not await self.redis_client.exists(RAFFLE_CONFIG_KEY):
            await interaction.response.send_message(
                "There is no currently-active raffle.", ephemeral=True
            )
            return
        participant_count = await self.redis_client.hlen(RAFFLE_SUBMISSIONS_KEY)
        await interaction.response.send_message(
            f"There are {participant_count} users in the raffle!\n"
            f"This corresponds to having a {100.0/participant_count}% chance to win any prize!"
        )

    @app_commands.command(
        name="remove",
        description="Remove a user from the current raffle.",
    )
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def raffle_remove(self, interaction: discord.Interaction, user: discord.User):
        was_removed = await self.redis_client.hdel(RAFFLE_SUBMISSIONS_KEY, user.name)
        response = (
            f"Removed {user.name} from the raffle!"
            if was_removed > 0
            else f"{user.name} not found in raffle."
        )
        await interaction.response.send_message(response)

    @app_commands.command(
        name="join", description="Join an upcoming raffle for fabulous prizes!"
    )
    async def join_raffle(self, interaction: discord.Interaction):
        member = interaction.user
        if member.bot:
            await interaction.response.send_message("No bots allowed!", ephemeral=True)
        if not await self.redis_client.exists(RAFFLE_CONFIG_KEY):
            await interaction.response.send_message(
                f"Sorry, {interaction.user.mention}, but there does not appear to be an active raffle!",
                ephemeral=True,
            )
            return
        if await self.redis_client.hexists(RAFFLE_SUBMISSIONS_KEY, member.name):
            raw_entry = await self.redis_client.hget(
                RAFFLE_SUBMISSIONS_KEY, member.name
            )
            entry = json.loads(raw_entry)
            entry["submissions"] += 1
            await self.redis_client.hset(
                RAFFLE_SUBMISSIONS_KEY, member.name, json.dumps(entry)
            )
            await interaction.response.send_message(
                "Your submission has been recorded!", ephemeral=True
            )
            return
        raffle_config = await self.redis_client.hgetall(RAFFLE_CONFIG_KEY)
        currtime = dt.datetime.now(tz=dt.timezone.utc)
        diff = currtime - member.joined_at
        diff_s = diff.total_seconds()
        days = divmod(diff_s, 86400)  # 86400 seconds in a day
        if days[0] < int(raffle_config["age"]):
            await interaction.response.send_message(
                f"Sorry, {interaction.user.global_name}, but your Discord account is not old enough to enter this raffle!"
            )
            await self.redis_client.hincrby(RAFFLE_CONFIG_KEY, "youth", 1)
            return
        # OTHERWISE
        entry = {
            "id": member.id,
            "submissions": 1,
            "entry": str(currtime),
            "hasWon": False,
        }
        await self.redis_client.hset(
            RAFFLE_SUBMISSIONS_KEY, member.name, json.dumps(entry)
        )
        await interaction.response.send_message(
            f"{interaction.user.global_name}, you have entered yourself into the {raffle_config['name']} raffle! Good luck!",
            ephemeral=True,
        )

    @app_commands.command(name="create", description="Create a raffle.")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def create_raffle(
        self,
        interaction: discord.Interaction,
        account_age: str,
        allow_multiple_wins: bool,
        name: str,
    ):
        if await self.redis_client.exists(RAFFLE_CONFIG_KEY):
            await interaction.response.send_message(
                f"Sorry, {interaction.user}, a raffle is already ongoing!"
            )
            return
        raffle_config = {
            "age": account_age,
            "name": name,
            "multiple": int(allow_multiple_wins),
            "youth": 0,
        }
        await self.redis_client.hset(RAFFLE_CONFIG_KEY, mapping=raffle_config)
        await interaction.response.send_message(f"Raffle {name} created.")

    @app_commands.command(name="close", description="Close an active raffle.")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def close_raffle(self, interaction: discord.Interaction):
        # Don't need to bother checking if there is a raffle...
        await self.redis_client.delete(RAFFLE_CONFIG_KEY, RAFFLE_SUBMISSIONS_KEY)
        await interaction.response.send_message("Raffle closed successfully.")

    @app_commands.command(name="pull", description="Pull a winner from the raffle!")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def pull_raffle(self, interaction: discord.Interaction, count: str = "1"):
        if not await self.redis_client.exists(RAFFLE_CONFIG_KEY):
            await interaction.response.send_message(
                "There is no currently-active raffle.", ephemeral=True
            )
            return
        responses = [
            "You have won a FABULOUS prize!\n",
            "You have been arbitrarily selected to receive stuff and things!\n",
            "You're a winner! But not of Scorv's stew, sorry. Enjoy the spoils of the raffle, though!\n",
            "You open your Discord and find...hot new loot!\n",
        ]
        """
        So, if we don't want people to be able to win multiple times, we will set their win-tracker to True if they've won.
        This will keep the while loop going on subsequent pulls.
        If we don't care, we'll never set their win-tracker to True, and therefore the if statement in the while loop will never trigger.
        """
        raffle_config = await self.redis_client.hgetall(RAFFLE_CONFIG_KEY)
        winners = []
        participant_count = await self.redis_client.hlen(RAFFLE_SUBMISSIONS_KEY)
        for winner in range(min(int(count), participant_count)):
            raffle_submissions = await self.redis_client.hgetall(RAFFLE_SUBMISSIONS_KEY)
            lucky = False
            lucky_entry = {}
            while not lucky:
                lucky = random.choice(list(raffle_submissions.keys()))
                lucky_entry = json.loads(raffle_submissions[lucky])
                if lucky_entry["hasWon"]:
                    lucky = False
            winners.append(
                f"<@{lucky_entry['id']}>, congratulations! {random.choice(responses)} A moderator will contact you shortly with information about your reward."
            )
            if not raffle_config["multiple"]:
                lucky_entry["hasWon"] = True
                await self.redis_client.hset(
                    RAFFLE_SUBMISSIONS_KEY, lucky, json.dumps(lucky_entry)
                )
        await interaction.response.send_message("\n\n".join(winners))
        return

    @app_commands.command(name="meme", description="Haha funny")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def meme_embed(self, interaction: discord.Interaction):
        if await self.redis_client.exists(RAFFLE_CONFIG_KEY):
            meme_embed = await self.create_embed(interaction)
            await interaction.response.send_message(embed=meme_embed)
        else:
            await interaction.response.send_message(
                "There is no currently-active raffle.", ephemeral=True
            )

    async def create_embed(self, interaction: discord.Interaction):
        raffle_embed = discord.Embed(
            title="Important Raffle Statistics", type="rich", color=0x00FFFF
        )
        raffle_embed.set_author(
            name=interaction.user, icon_url=interaction.user.avatar.url
        )
        spamCount = 0
        highest = (0, "")
        raffle_submissions = await self.redis_client.hgetall(RAFFLE_SUBMISSIONS_KEY)
        for user, raw_entry in raffle_submissions.items():
            entry = json.loads(raw_entry)
            subCount = entry["submissions"]
            if subCount > 1:
                spamCount += 1
                if subCount > highest[0]:
                    highest = (subCount, user)
        raffle_embed.add_field(
            name="People that tried to abuse the system:", value=spamCount, inline=False
        )
        if spamCount > 0:
            raffle_embed.add_field(
                name="Biggest tryhard:",
                value=f"{highest[1]} at {highest[0]} extraneous resubmissions.",
                inline=False,
            )
        raffle_config = await self.redis_client.hgetall(RAFFLE_CONFIG_KEY)
        raffle_embed.add_field(
            name="Attempted Underage Gamblers:",
            value=raffle_config["youth"],
        )

        return raffle_embed
