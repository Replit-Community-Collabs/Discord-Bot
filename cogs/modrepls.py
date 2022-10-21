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
    await ctx.send(f"Yes test works and cogs work!!!")
    

async def setup(client):
  await client.add_cog(test(client))
