from PIL import Image
import discord
from discord import app_commands
from discord.ext import commands
import os


@app_commands.guild_only()
class MiscCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="mobile")
    async def mobile_image(self, interaction: discord.Interaction, user: discord.User):
        avatar = user.avatar
        if avatar.is_animated():
            return
        else:
            fn = str(user.id) + "_temp.png"
            fn_o = "mobile_output.png"
            await avatar.save(fn)

            icon = Image.open(fn)
            self.build_mobile_frame(icon, fn_o)

            await interaction.response.send_message(
                file=discord.File(fp=fn_o)
            )

            if os.path.exists(fn):
                os.remove(fn)
            else:
                print(f"Error occurred when deleting file:\t{fn}")
            if os.path.exists(fn_o):
                os.remove(fn_o)
            else:
                print(f"Error occurred when deleting file:\t{fn_o}")

    def build_mobile_frame(self, icon, output_fn):
        mobile_discord = Image.open("images/MobileDiscord.png")
        iresize = icon.resize((43, 43), Image.LANCZOS)
        x1, y1 = 221, 148
        x2, y2 = 264, 191
        mask = iresize.convert("RGBA")
        mobile_discord.paste(iresize, (x1, y1, x2, y2), mask)
        mobile_discord.save(output_fn)
        return output_fn
