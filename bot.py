import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils import create_embed, handle_error

import os
import sys

load_dotenv()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='r!', intents=intents, application_id=1032306356692205578)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print("Ready")
    activity = discord.Activity(type=discord.ActivityType.watching, name="Repls.best | Prefix: 'r!'")
    await bot.change_presence(status=discord.Status.online, activity=activity)


@tree.command()
async def kill(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(embed=await create_embed())
        return
    await ctx.send(
        embed=await create_embed(
            title="Restarting", description=f"Restart ordered by {ctx.author.mention}"
        )
    )

    sys.exit()
    
@kill.error
async def kill_error_handler(ctx, error):
    await handle_error(ctx, error)

@bot.command(aliases=["pong", "p"]) #ping
async def ping(ctx):
    await ctx.send(
        embed=await create_embed(
            title="Pong", description=f":ping_pong: Pong, latancy: {round(bot.latency *1000, 2)}", color=discord.Color.green()
        )
    )


try:
    bot.run(os.environ["BOT_TOKEN"])
except Exeption as e:
    print(f"ERROR WITH LOGING IN: {e}")