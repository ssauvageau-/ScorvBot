import os

import discord
import requests

import discord
from discord import app_commands
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch


@app_commands.guild_only()
class TwitchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.bot = bot
        self.guild_prime = os.getenv("PRIMARY_GUILD")
        self.guild_test = os.getenv("TEST_GUILD")
        self.env = os.getenv("ENV")
        self.twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_secret = os.getenv("TWITCH_SECRET")
        self.twitch = Twitch(self.twitch_client_id, self.twitch_secret)
        # self.twitch.authenticate_app([])
        self.TWITCH_STREAM_API_ENDPOINT_V5 = os.getenv("TWITCH_ENDPOINT")
        # self.API_HEADERS = {
        #     'Client-ID': self.twitch_client_id,
        #     'Accept': 'application/vnd.twitchtv.v5+json',
        # }
        # self.reqSession = requests.Session()
        self.runTest = ""
        if self.runTest:
            self.test.start()
        super().__init__()

    @app_commands.command(
        name="livenow", description="See who is currently live on twitch!"
    )
    async def TwitchLive(self, interaction: discord.Interaction):
        gd_id = 26881
        body = {
            "client_id": self.twitch_client_id,
            "client_secret": self.twitch_secret,
            "grant_type": "client_credentials",
        }
        req = requests.post("https://id.twitch.tv/oauth2/token", body)

        keys = req.json()

        headers = {
            "Client-ID": self.twitch_client_id,
            "Authorization": "Bearer " + keys["access_token"],
        }
        streams = requests.get(
            f"https://api.twitch.tv/helix/streams?game_id={gd_id}", headers=headers
        )
        live = streams.json()
        data = live["data"]
        if len(data) == 0:
            await interaction.response.send_message(
                "Sorry, but there do not appear to be any live Grim Dawn Streams currently!",
                ephemeral=True,
            )
            return
        await interaction.response.send_message(
            "Posting the list of live Grim Dawn streams below:"
        )
        ts = interaction.created_at
        col = interaction.user.color
        embed_size_limit = 25
        chunked = [
            data[i : i + embed_size_limit]
            for i in range(0, len(data), embed_size_limit)
        ]
        for chunk in chunked:
            streamEmbed = discord.Embed(color=col, timestamp=ts)
            streamEmbed.set_author(
                name="Grim Dawn on Twitch",
                url="https://www.twitch.tv/directory/category/grim-dawn",
                icon_url="https://static-cdn.jtvnw.net/ttv-boxart/26881_IGDB-144x192.jpg",
            )
            for stream in chunk:
                streamEmbed.add_field(
                    name=stream["user_name"],
                    value=f'{stream["title"]}\nBeing streamed to {stream["viewer_count"]} viewers.\nWatch here: https://twitch.tv/{stream["user_login"]}',
                    inline=True,
                )
            await interaction.channel.send(embed=streamEmbed)

    # only used if self.runTest != ""
    @tasks.loop(seconds=1, count=1)
    async def test(self):
        twitch_user = "gorgc"
        body = {
            "client_id": self.twitch_client_id,
            "client_secret": self.twitch_secret,
            "grant_type": "client_credentials",
        }
        req = requests.post("https://id.twitch.tv/oauth2/token", body)

        keys = req.json()

        headers = {
            "Client-ID": self.twitch_client_id,
            "Authorization": "Bearer " + keys["access_token"],
        }
        stream = requests.get(
            "https://api.twitch.tv/helix/streams?user_login=" + twitch_user,
            headers=headers,
        )
        stream_data = stream.json()

        if len(stream_data["data"]) == 1:
            title = stream_data["data"][0]["title"]
            game = stream_data["data"][0]["game_name"]
            if self.env is "prod":
                guild = await self.bot.fetch_guild(self.guild_prime)
            elif self.env is "dev":
                guild = await self.bot.fetch_guild(self.guild_test)
            channels = await guild.fetch_channels()
            tmp_embed = discord.Embed(color=discord.Color.gold())
            tmp_embed.set_footer(text=game)
            tmp_embed.add_field(
                name=f"https://www.twitch.tv/{twitch_user}", value=title, inline=True
            )
            # tmp_embed.add_field(name="", value=f'https://www.twitch.tv/{twitch_user}', inline=True)
            for channel in channels:
                if type(channel) is discord.TextChannel and channel.name == "general":
                    await channel.send(embed=tmp_embed)
        else:
            print(f"{twitch_user} is not live")
