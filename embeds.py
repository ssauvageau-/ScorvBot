import discord

welcome_embed = discord.Embed(color=0x1E1F22)
welcome_embed.add_field(
    name="Welcome to the Community Grim Dawn Discord Server",
    value="Grim Dawn is an ARPG set inside a apocalyptic fantasy world where humanity is on the brink of extinction, "
    "iron is valued above gold and trust is hard earned. Grim Dawn features complex character development, "
    "hundreds of unique items, crafting, and quests with choice & consequence.",
    inline=False,
)
welcome_text = "# Welcome to the Community Grim Dawn Discord Server"
global_text = (
    "## Global Server Rules"
    "\n1. Keep discussions civil and respect the ideas of others even if you disagree with them. Hate speech and any kind of discrimination will not be tolerated - this includes (but is not limited to) any form of racism, homophobia, transphobia, sexism, xenophobia, or blatant disrespect."
    "\n2. Please keep all discussions on the server in English, as this is the language spoken by all moderation staff."
    "\n3. Posting pornographic, disturbing, illegal images/links is strictly prohibited. Examples of such prohibited content include, but are not limited to: real or disturbing depictions of violence; content that exploits children in any way and sexually explicit content. Please notify a <@&137735685674106880> of any such content violations."
    "\n4. Engagement in/promotion of unlawful activity is strictly prohibited. Examples of such prohibited activity include, but are not limited to: exploiting minors; stealing; encouraging real-world violence; engaging in fraud; piracy; hacking; breaking copyright laws. Discussion of piracy is prohibited, and no support will be given for issues arising from use of a pirated game copy. Please notify a <@&137735685674106880> of any such violations."
)
global_text2 = (
    "5. Let the moderators handle all moderation duties. If you find an issue, please notify a <@&137735685674106880> to ping them and let them handle the issue. Entangling yourself in the issue will only cause more disruption. Disagreements in DM's should be handled by users themselves (block if necessary). Exceptions to this are: 1) scam attempts, and 2) users trying to circumvent moderation on the server by taking harassment to DM's instead. In such cases, **please DM a moderator with screenshots of the conversation**. All reported issues will be handled on a case-by-case basis."
    "\n6. Do not advertise or encourage anything that is against the TOS/EULA of Grim Dawn. Respect the Terms of Service & Guidelines of Discord - <https://discord.com/terms> | <https://discord.com/guidelines>"
    "\n7. Do not advertise any kind of Discord/community/campaign or other links without permission. Users have global permission to post the links below at-will within reasonable contexts."
    "\n8. Political discussions and topics shall be kept short or entirely avoided if possible in all channels."
    "\n\nFinally, please submit any bug reports for the game on the [official forums](<https://forums.crateentertainment.com/c/grimdawn/bug-reporting/27>) or by emailing Crate Entertainment directly at <support@crateentertainment.com>."
)
global_text3 = (
    "### ↓Whitelisted Discord Links↓"
    "\n**Grim Dawn** (you are here)"
    "\n* <https://discord.gg/8Dr8mge>"
    "\n**Farthest Frontier**"
    "\n* <https://discord.gg/WbBWWuAYjh>"
    "\n**Grim Dawn League**"
    "\n* <https://discord.gg/n94PcmV>"
    "\n**Grimarillion & DoM Community**"
    "\n* <https://discordapp.com/invite/GNqqDUz>"
    "\n**Dammitt's Tools**"
    "\n* <https://discord.gg/8uEhMAkxHc>"
)
global_embed = discord.Embed(color=0x1E1F22)
global_embed.add_field(
    name="Global Rules",
    value="**1**. Follow the rules outlined below for the various channels."
    "\n**2**. Keep discussions civil and respect the ideas of others even if you disagree with them. Hate speech and "
    "any kind of discrimination will not be tolerated. "
    "\n**3**. Please keep all discussions on the server in English, as this is the language spoken by all moderation staff. "
    "\n**4**. Posting pornographic, disturbing, illegal images/links is strictly prohibited. Examples of such "
    "prohibited content include, but are not limited to: real or disturbing depictions of violence; content "
    "that exploits children in any way and sexually explicit content. "
    "\n**5**. Engagement in/promotion of unlawful activity is strictly prohibited. Examples of such prohibited "
    "activity include, but are not limited to: exploiting minors; stealing; encouraging real-world violence; "
    "engaging in fraud; piracy; hacking; breaking copyright laws. Discussion of piracy is prohibited, "
    "and no support will be given for issues arising from use of a pirated game copy. ",
    inline=False,
)
global_embed2 = discord.Embed(color=0x1E1F22)
global_embed2.add_field(
    name="",
    value="\n**6**. Let the moderators handle all moderation duties. If you find an issue, please use the "
    "<@&137735685674106880> tag to ping them and let them handle the issue. Entangling yourself in the issue "
    'will only cause more disruption. Disagreements in DM\'s should be handled by users themselves ("block" if '
    "necessary). Exceptions to this are: 1) scam attempts, and 2) users trying to circumvent moderation on the "
    "server by taking harassment to DM's instead. In such cases, **please DM a moderator with screenshots of the "
    "conversation**. All reported issues will be handled on a case-by-case basis. "
    "\n**7**. Do not advertise or encourage anything that is against the TOS/EULA of Grim Dawn. Respect the Terms of "
    "Service & Guidelines of Discord - https://discord.com/terms | https://discord.com/guidelines "
    "\n**8**. Do not advertise any kind of Discord/community/campaign or other links without permission. Users have "
    "global permission to post the links below at-will within reasonable contexts."
    "\n**9**. Political discussions and topics shall be kept short or entirely avoided if possible in all channels.",
)
global_embed3 = discord.Embed(color=0x1E1F22)
global_embed3.add_field(
    name="",
    value="**↓Whitelisted Discord Links↓**:"
    "\n**Grim Dawn** (you are here)"
    "\nhttps://discord.gg/8Dr8mge"
    "\n**Farthest Frontier**"
    "\nhttps://discord.gg/WbBWWuAYjh"
    "\n**Grim Dawn League"
    "\nhttps://discord.gg/n94PcmV"
    "\n**Grimarillion & DoM Community"
    "\nhttps://discordapp.com/invite/GNqqDUz"
    "\n**Reign of Terror Mod Discord"
    "\nhttps://discord.gg/eSRNSqGk22"
    "\n**Dammitt's Tools"
    "\nhttps://discord.gg/8uEhMAkxHc",
)
channel_news_embed = discord.Embed(color=0x1E1F22)
channel_news_embed.add_field(
    name="Global",
    value="<#137741704944943105>"
    "\nNews about recent important events related to Grim Dawn."
    "\n<#1150483398754836530>"
    "\nThis channel will be updated with updates to this server.",
    inline=False,
)
channel_offtopic_embed = discord.Embed(color=0x1E1F22)
channel_offtopic_embed.add_field(
    name="↓ Offtopic ↓",
    value="<#119758608765288449>"
    "\nFor discussion of other games unrelated to Grim Dawn."
    "\n<#144781923590471680>"
    "\nEverything is allowed within range of the rules but use common sense."
    "\n<#602362713863094322>"
    "\nChannel archived for month of September. See https://discord.com/channels/119758608765288449/1150483398754836530/1276164130251739166"
    "\n<#653698423945560075>"
    "\nFor sharing and discussing music, commonly through YouTube.",
    inline=False,
)
channel_gd_embed = discord.Embed(color=0x1E1F22)
channel_gd_embed.add_field(
    name="↓ Grim Dawn ↓",
    value="<#340206431070322692>"
    "\nIs only meant to be about Grim Dawn."
    "\n<#474470028503285762>"
    "\nClosed community, open topic channel for <@&474151602454921218> members."
    "\n<#282754266123206657>"
    "\nThis channel is for Grim Dawn build discussions and helping each other with game related questions based "
    "on making your characters."
    "\n<#309941110128771073>"
    "\nAll about Grim Dawn mods and everything related."
    "\n(Other channels are not restricted to talk about mods for Grim Dawn.)",
    inline=False,
)
channel_community_embed = discord.Embed(color=0x1E1F22)
channel_community_embed.add_field(
    name="↓ Community ↓",
    value="<#1152658400421875732>"
    "\nThis forum channel is for trading with other players. See the channel's posting guidelines for more information."
    "\n<#1152659580552224818>"
    "\nThis forum channel is for finding players to group up with. See the channel's posting guidelines for more information."
    "\n<#1153388417187590285>"
    "\nThis forum channel is for showing off your character. See the channel's posting guidelines for more information."
    "\n<#1153390164886958212>"
    "\nThis forum channel is for showing off rare or noteworthy item drops. See the channel's posting guidelines for more information.",
    inline=False,
)
chat_roles_embed = discord.Embed(color=0x1E1F22)
chat_roles_embed.add_field(
    name="",
    value="<@&241956541446619136>"
    "\nThe manager of this Discord server."
    "\nThis server's Discord moderation is not affiliated with Crate Entertainment."
    "\n<@&137735685674106880>"
    "\nHelps you with questions and keeps the Discord chat clean."
    "\n<@&351387211356438528>"
    "\nOur cleaning crew that enforces mostly channel rules."
    "\n<@&237159960566300672>"
    "\nOfficial Grim Dawn Forum moderator."
    "\n<@&340265796980703234>"
    "\nLong term community members with access to alpha versions of Grim Dawn to provide feedback and game testing results."
    "\nMost of them are giga-nerds."
    "\n<@&474151602454921218>"
    "\nPeople that have verified their forum account. Ask a moderator for instructions on how to do so if interested.",
    inline=False,
)
buy_gd_embed = discord.Embed(color=0x322D28)
buy_gd_embed.add_field(
    name="",
    value="**Official Grim Dawn Website**"
    "\nhttps://www.grimdawn.com/"
    "\n**Steam**"
    "\nhttps://store.steampowered.com/app/219990/Grim_Dawn/"
    "\n**Humble Bundle**"
    "\nhttps://www.humblebundle.com/store/grim-dawn"
    "\n**GOG**"
    "\nhttps://www.gog.com/en/game/grim_dawn",
    inline=True,
)
buy_gd_embed.set_image(
    url="https://media.discordapp.net/attachments/426464234994532364/557061415827931148/GD2.png"
)
buy_gd_embed.set_thumbnail(
    url="https://media.discordapp.net/attachments/426464234994532364/557061415827931148/GD2.png"
)
buy_aom_embed = discord.Embed(color=0x1D8863)
buy_aom_embed.add_field(
    name="",
    value="**Steam**"
    "\nhttps://store.steampowered.com/app/642280/Grim_Dawn__Ashes_of_Malmouth_Expansion/"
    "\n**Humble Bundle**"
    "\nhttps://www.humblebundle.com/store/grim-dawn-ashes-of-malmouth-expansion"
    "\n**GOG**"
    "\nhttps://www.gog.com/en/game/grim_dawn_ashes_of_malmouth",
    inline=True,
)
buy_aom_embed.set_image(
    url="https://media.discordapp.net/attachments/426464234994532364/557059808361054210/gdheaderboxtop_2.png"
)
buy_aom_embed.set_thumbnail(
    url="https://media.discordapp.net/attachments/426464234994532364/557059628802768897/aom_icon.png"
)
buy_fg_embed = discord.Embed(color=0xFFA647)
buy_fg_embed.add_field(
    name="",
    value="**Steam**"
    "\nhttps://store.steampowered.com/app/897670/Grim_Dawn__Forgotten_Gods_Expansion/"
    "\n**Humble Bundle**"
    "\nhttps://www.humblebundle.com/store/grim-dawn-forgotten-gods-expansion"
    "\n**GOG**"
    "\nhttps://www.gog.com/en/game/grim_dawn_forgotten_gods",
    inline=True,
)
buy_fg_embed.set_image(
    url="https://media.discordapp.net/attachments/426464234994532364/557059372161957898/grimdawndiscordfg.png"
)
buy_fg_embed.set_thumbnail(
    url="https://media.discordapp.net/attachments/426464234994532364/557059472254566410/Grim_Dawn_0000.png"
)
buy_foa_embed = discord.Embed(color=0x60FFFC)
buy_foa_embed.add_field(
    name="",
    value="**Steam**"
    "\nArriving Posthaste!"
    "\n**Humble Bundle**"
    "\nArriving Posthaste!"
    "\n**GOG**"
    "\nArriving Posthaste!",
    inline=True,
)
buy_foa_embed.set_image(
    url="https://cdn.discordapp.com/attachments/428832869398347776/1151193901013667880/cropped-gdx3_headerboxtop.png"
)
buy_foa_embed.set_thumbnail(
    url="https://cdn.discordapp.com/attachments/428832869398347776/1151193829869891739/gdx3_GD_icon_1.png"
)
links_embed = discord.Embed(color=0x1E1F22)
links_embed.add_field(
    name="",
    value="**Official Links**"
    "\nGrim Dawn Forum"
    "\nhttps://forums.crateentertainment.com/c/grimdawn/"
    "\nGrim Dawn Builds"
    "\nhttps://forums.crateentertainment.com/c/grimdawn/classes-skills-and-builds/21"
    "\nGrim Dawn SubReddit"
    "\nhttps://www.reddit.com/r/Grimdawn/"
    "\nGrim Dawn Wikipedia"
    "\nhttps://grimdawn.fandom.com/wiki/Grim_Dawn_Wiki"
    "\nGrim Dawn Community Highlights"
    "\nhttps://www.grimdawn.com/community/"
    "\n"
    "\n**Useful Links**"
    "\nGrim Dawn Online Map"
    "\nhttps://www.grimtools.com/map/"
    "\nGrim Dawn Build Compendium"
    "\nhttps://forums.crateentertainment.com/t/build-compendiums/82060"
    "\nGrim Dawn F.A.Q"
    "\nhttps://tinyurl.com/n676c8y"
    "\nCharacter Builder/Planner"
    "\nhttp://www.grimtools.com/calc/"
    "\nItem Database"
    "\nhttps://www.grimtools.com/db/items/"
    "\nMonster Database"
    "\nhttps://www.grimtools.com/monsterdb/"
    "\nResistance Reduction Cheat Sheet"
    "\nhttps://tinyurl.com/yya5hmo2",
)
