#imports
from discord.ext import commands
from discord import app_commands
import discord
import datetime
from utils import create_embed, handle_error


class test(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command() 
  async def test(self,ctx):
    embed = create_embed(title="TEST", description="Yes! test command works and cogs work!!! (still gotta figure out how to do it with slash commands...")
    await ctx.send(embed=embed)
    

async def setup(client):
  await client.add_cog(test(client))
