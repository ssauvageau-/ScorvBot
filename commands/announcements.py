import discord
from discord import app_commands
from discord.ext import commands
import embeds

COMMAND_WHITELIST = ["Admin", "Moderator"]


@app_commands.guild_only()
class AnnouncementCommandGroup(app_commands.Group, name="announcements"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="post-rules", description="Post the generated rules")
    @app_commands.describe(channel="The channel in which to post the rules")
    @app_commands.checks.has_any_role(COMMAND_WHITELIST)
    async def post_rules(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.defer(thinking=True)
        await channel.purge()
        await channel.send(
            "https://cdn.discordapp.com/attachments/428832869398347776/1151199255990640721/Grim_Dawn_Discord_Logo.png"
        )
        await channel.send(
            "https://cdn.discordapp.com/attachments/647753999948185611/647754106492026902/2a8e119d-e266-40d3-a9c8-a92194b658472Fdivider2.png"
        )
        await channel.send(embed=embeds.welcome_embed)
        await channel.send(
            "https://cdn.discordapp.com/attachments/647753999948185611/647754112661848094/2a8e119d-e266-40d3-a9c8-a92194b658472Fatt.png"
        )
        await channel.send(embed=embeds.global_embed)
        await channel.send(embed=embeds.global_embed2)
        await channel.send(
            "https://cdn.discordapp.com/attachments/647753999948185611/647754128541614090/2a8e119d-e266-40d3-a9c8-a92194b658472Fchannel_rules.png"
        )
        await channel.send(
            embeds=[
                embeds.channel_news_embed,
                embeds.channel_gd_embed,
                embeds.channel_community_embed,
                embeds.channel_offtopic_embed,
            ]
        )
        await channel.send(
            "https://cdn.discordapp.com/attachments/647753999948185611/647754159034204160/2a8e119d-e266-40d3-a9c8-a92194b658472Fchat_roles.png"
        )
        await channel.send(embed=embeds.chat_roles_embed)
        await interaction.followup.send(f"Posted rules in {channel.mention}")

    @app_commands.command(name="post-links", description="Post the generated links")
    @app_commands.describe(channel="The channel in which to post the links")
    @app_commands.checks.has_any_role(COMMAND_WHITELIST)
    async def post_links(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.defer(thinking=True)
        await channel.purge()
        await channel.send(
            "https://cdn.discordapp.com/attachments/647753999948185611/647754188469567488/2a8e119d-e266-40d3-a9c8-a92194b658472Fbuy_now.png"
        )
        await channel.send(
            embeds=[
                embeds.buy_gd_embed,
                embeds.buy_aom_embed,
                embeds.buy_fg_embed,
                embeds.buy_foa_embed,
            ]
        )
        await channel.send(
            "https://cdn.discordapp.com/attachments/647753999948185611/647754218198925312/2a8e119d-e266-40d3-a9c8-a92194b658472Flinkbase.png"
        )
        await channel.send(embed=embeds.links_embed)
        await interaction.followup.send(f"Posted links in {channel.mention}")

    @post_rules.error
    @post_links.error
    async def missing_role_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.errors.MissingAnyRole):
            await interaction.response.send_message(
                "You do not have the required permissions to use this command!",
                ephemeral=True,
            )
        else:
            raise error
