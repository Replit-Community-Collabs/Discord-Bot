import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils import create_embed, handle_error

import os
import sys

load_dotenv()

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
    activity = discord.Activity(type=discord.ActivityType.watching, name="Repls.best | Prefix: 'r!'")
    await bot.change_presence(status=discord.Status.online, activity=activity)


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

@bot.hybrid_command(name='ping', description='Check bot latency', with_app_command=True, aliases=["pong", "p"])
async def ping(ctx):
    await ctx.defer(ephemeral=True)
    await ctx.reply(
        embed=await create_embed(
            title="Pong", description=f":ping_pong: Pong! :ping_pong:\nLatency: {round(bot.latency *1000, 2)}ms!", color=discord.Color.green()
        )
    )

    
    

try:
    bot.run(os.environ["BOT_TOKEN"])
except Exeption as e:
    print(f"ERROR WITH LOGING IN: {e}")
