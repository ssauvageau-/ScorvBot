from PIL import Image, ImageSequence
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
        fn = str(user.id) + "_temp"
        fn_o = "mobile_output.gif"
        frame_list = []
        await avatar.save(fn)
        with Image.open(fn) as im:
            idx = 1
            duration = 0

            for frame in ImageSequence.Iterator(im):
                frame_list.append(self.build_mobile_frame(frame))
                idx += 1
                try:
                    duration += im.info["duration"]
                except KeyError:
                    continue

            frame_duration = int(idx / duration) if duration > 0 else 1000

        frame_list[0].save(
            fn_o,
            save_all=True,
            append_images=frame_list[1:],
            optimize=False,
            duration=frame_duration,
            loop=0,
        )

        await interaction.response.send_message(file=discord.File(fp=fn_o))

        if os.path.exists(fn):
            os.remove(fn)
        else:
            print(f"Error occurred when deleting file:\t{fn}")
        if os.path.exists(fn_o):
            os.remove(fn_o)
        else:
            print(f"Error occurred when deleting file:\t{fn_o}")

    def build_mobile_frame(self, icon):
        mobile_discord = Image.open("images/MobileDiscord.png")
        iresize = icon.resize((43, 43), Image.LANCZOS)
        x1, y1 = 221, 148
        x2, y2 = 264, 191
        mask = iresize.convert("RGBA")
        mobile_discord.paste(iresize, (x1, y1, x2, y2), mask)
        return mobile_discord
