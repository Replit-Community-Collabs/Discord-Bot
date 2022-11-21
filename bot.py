import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils import create_embed, handle_error

import os
import sys
import time
import random
import json

FLOOP_CHANNELS = [
    [1032000304343961630, False],
    [1031690140025880660, True],
    [1032305788494037082, True],
]

load_dotenv()
cogs = ["cogs.modrepls"]


class Bot(commands.Bot):  # cogs :eyes:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="r!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

    async def on_command_error(self, ctx, error):
        await handle_error(ctx, error, ephemeral=True)


bot = Bot()


@bot.event
async def on_ready():
    print("Ready")
    activity = discord.Activity(
        type=discord.ActivityType.watching, name="Repls.best, 'r!' and /"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.hybrid_command(
    name="restart", with_app_command=True, description="Restart the bot"
)
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.defer(ephemeral=True)
    if not ctx.author.guild_permissions.administrator:
        await ctx.reply(embed=await create_embed())
        return
    # if ctx.author.id == 991791436662046800:
    #     await ctx.reply("No")
    #     return
    await ctx.reply(
        embed=await create_embed(
            title="Restarting", description=f"Restart ordered by {ctx.author.mention}"
        )
    )

    sys.exit()


@bot.hybrid_command(
    name="ping",
    description="Check bot latency",
    with_app_command=True,
    aliases=["pong", "p"],
)  # extra pong code I had e lying around somewhere
async def ping(ctx):
    await ctx.defer(ephemeral=True)
    if round(bot.latency * 1000) <= 50:
        embed = discord.Embed(
            title="PING",
            description=f":ping_pong: Pong! Bot's latency  is **{(bot.latency *1000)}** ms!",
            color=0x44FF44,
        )
    elif round(bot.latency * 1000) <= 100:
        embed = discord.Embed(
            title="PING",
            description=f":ping_pong: Pong! Bot's latency  is **{round(bot.latency *1000)}** ms!",
            color=0xFFD000,
        )
    elif round(bot.latency * 1000) <= 200:
        embed = discord.Embed(
            title="PING",
            description=f":ping_pong: Pong! Bot's latency  is **{round(bot.latency *1000)}** ms!",
            color=0xFF6600,
        )
    else:
        embed = discord.Embed(
            title="PING",
            description=f":ping_pong: Pong! Bot's latency  is **{round(bot.latency *1000)}** ms!",
            color=0x990000,
        )
    await ctx.reply(embed=embed)


@bot.hybrid_command(
    with_app_command=True,
    name="floop",
    description="Floop the specified user a certain amount of times",
)
async def floop(ctx, user: discord.Member, amount: int = 10):
    if user.id == 915670836357247006:
        await ctx.reply("No")
        return
    elif user.bot:
        await ctx.reply("How do you expect me to floop a bot?")
        return
    elif amount > 1000:
        await ctx.reply("That's too many floops!")
        return
    for i in range(amount):
        if random.randint(1, 2) == 1:
            channels = [c[0] for c in FLOOP_CHANNELS]
            channel = bot.get_channel(random.choice(channels))
            time.sleep(random.randint(0, 27))
            webhook = await channel.create_webhook(name="Floop")
            msg = await webhook.send(
                f"FLOOP #{i + 1} - {user.mention} from {ctx.author.name}", wait=True
            )
            if [channel.id, True] in FLOOP_CHANNELS:
                await webhook.delete_message(msg.id)
            await webhook.delete()
        else:
            try:
                await user.send(f"FLOOP #{i + 1} - {ctx.author.name} flooped you!")
            except:
                channels = [c[0] for c in FLOOP_CHANNELS]
                channel = bot.get_channel(random.choice(channels))
                time.sleep(random.randint(0, 27))
                webhook = await channel.create_webhook(name="Floop")
                msg = await webhook.send(
                    f"FLOOP #{i + 1} - {user.mention} from {ctx.author.name}", wait=True
                )
                if [channel.id, True] in FLOOP_CHANNELS:
                    await webhook.delete_message(msg.id)
                await webhook.delete()

    await ctx.reply(f"Flooped {user.mention} {amount} times!")


try:
    bot.run(os.environ["BOT_TOKEN"])
except Exception as e:
    print(f"ERROR WITH LOGING IN: {e}")
