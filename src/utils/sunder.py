import os

import discord
from PIL import Image, ImageSequence
from typing import Tuple


class Sunder:
    def __init__(self, member: discord.Member):
        self.member = member
        self.output_file_name = f"sunder_{self.member.id}.gif"
        self.avatar_file_name = f"{self.member.id}_avatar.gif"
        self.sunder_path = "images/SunderSquare.png"
        self.embed = discord.Embed(
            color=discord.Color.red(),
            title=f"_**{self.member.display_name.upper()} HAS BEEN SUNDERED!**_",
        )

    async def generate_embed(self) -> None:
        saved_bytes = await self.member.avatar.save(self.avatar_file_name)
        if saved_bytes == 0:
            raise Exception("Failed to download avatar")

        with Image.open(self.avatar_file_name) as avatar, Image.open(
            self.sunder_path
        ) as sunder_frame:
            avatar_resized = avatar.resize((256, 256), Image.LANCZOS)
            frames = []
            total_duration = 0
            frame_count = 0
            for i, frame in enumerate(ImageSequence.Iterator(avatar_resized), start=1):
                frame_count = i
                # Paste sunder on top of avatar frame
                mask = sunder_frame.convert("RGBA")
                frame.paste(sunder_frame, mask=mask)
                frames.append(frame)

                # Get duration of frame
                duration = frame.info.get("duration") or 0
                total_duration += duration

            frame_duration = (
                int(frame_count / total_duration) if total_duration > 0 else 1000
            )

            frames[0].save(
                self.output_file_name,
                save_all=True,
                append_images=frames[1:],
                optimize=False,
                duration=frame_duration,
                loop=0,
            )

            self.file = discord.File(self.output_file_name)
            self.embed.set_image(url=f"attachment://{self.output_file_name}")

    async def __aenter__(self) -> Tuple[discord.File, discord.Embed]:
        await self.generate_embed()
        return self.file, self.embed

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        if os.path.exists(self.avatar_file_name):
            os.remove(self.avatar_file_name)
        else:
            print(f"Error occurred when deleting file:\t{self.avatar_file_name}")
        if os.path.exists(self.output_file_name):
            os.remove(self.output_file_name)
        else:
            print(f"Error occurred when deleting file:\t{self.output_file_name}")
