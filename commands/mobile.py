from PIL import Image
import discord
from discord import app_commands
from discord.ext import commands
import os


@app_commands.guild_only()
class MobileCommandGroup(app_commands.Group, name="mobile"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="-")
    async def mobile_image(self, interaction: discord.Interaction, user: discord.User):
        avatar = user.avatar
        if not avatar.is_animated():
            fn = str(user.id) + "_temp.png"
            fn_o = "mobile_output.png"
            await avatar.save(fn)

            mobile_discord = Image.open("images/MobileDiscord.png")
            icon = Image.open(fn)
            iresize = icon.resize((43, 43), Image.LANCZOS)
            x1, y1 = 221, 148
            x2, y2 = 264, 191
            mask = iresize.convert("RGBA")
            mobile_discord.paste(iresize, (x1, y1, x2, y2), mask)
            mobile_discord.save(fn_o)

            await interaction.response.send_message(file=discord.File(fp="mobile_output.png"))

            if os.path.exists(fn):
                os.remove(fn)
            else:
                print(f"Error occurred when deleting file:\t{fn}")
            if os.path.exists(fn_o):
                os.remove(fn_o)
            else:
                print(f"Error occurred when deleting file:\t{fn_o}")
