import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils import create_embed, handle_error

import os
import sys

load_dotenv()
cogs = ["cogs.modrepls"]

class Bot(commands.Bot): #cogs :eyes:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="r!", intents=intents
        )

    async def setup_hook(self):
        await self.tree.sync()
        print(f'Synced slash commands for {self.user}')

    async def on_command_error(self, ctx, error):
        await handle_error(ctx, error, ephemeral=True)


bot = Bot()

@bot.event
async def on_ready():
    print("Ready")
    activity = discord.Activity(type=discord.ActivityType.watching, name="Repls.best, 'r!' and /")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
         await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.hybrid_command(name='restart', with_app_command=True, description='Restart the bot')
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.defer(ephemeral=True)
    if not ctx.author.guild_permissions.administrator:
        await ctx.reply(embed=await create_embed())
        return
    await ctx.reply(
        embed=await create_embed(
            title="Restarting", description=f"Restart ordered by {ctx.author.mention}"
        )
    )

    sys.exit()

@bot.hybrid_command(name='ping', description='Check bot latency', with_app_command=True, aliases=["pong", "p"]) #extra pong code I had e lying around somewhere
async def ping(ctx):
    await ctx.defer(ephemeral=True)
    if round(bot.latency * 1000) <= 50:
        embed = discord.Embed(
            title="PING",
            description=
            f":ping_pong: Pong! Bot's latency  is **{(bot.latency *1000)}** ms!",
            color=0x44ff44)
    elif round(bot.latency * 1000) <= 100:
        embed = discord.Embed(
            title="PING",
            description=
            f":ping_pong: Pong! Bot's latency  is **{round(bot.latency *1000)}** ms!",
            color=0xffd000)
    elif round(bot.latency * 1000) <= 200:
        embed = discord.Embed(
            title="PING",
            description=
            f":ping_pong: Pong! Bot's latency  is **{round(bot.latency *1000)}** ms!",
            color=0xff6600)
    else:
        embed = discord.Embed(
            title="PING",
            description=
            f":ping_pong: Pong! Bot's latency  is **{round(bot.latency *1000)}** ms!",
            color=0x990000)
    await ctx.reply(embed=embed)




try:
    bot.run(os.environ["BOT_TOKEN"])
except Exeption as e:
    print(f"ERROR WITH LOGING IN: {e}")
