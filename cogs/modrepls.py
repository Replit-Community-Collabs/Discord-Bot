#imports
from discord.ext import commands
from discord import app_commands
import discord
from utils import create_embed, handle_error


class kick(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command() # Kick command. Not like we need it but its a placeholder/example for cogs
  async def kick(self,ctx, member: discord.Member, *, reason=None):
    await ctx.guild.kick(member)
    await member.send(f"You have been kicked from RCC. Reason:\n```\n{reason}\n```")
    await ctx.send(f"succesfully kicked {member}")
    channel = self.client.get_channel(982299411751256064)
    embed = discord.Embed(title=f"**{member}** was kicked", description=
    f"**by:** {ctx.message.author}\n**reason:** {reason}",
    timestamp=datetime.now(),
    color=discord.Colour.purple())
    await channel.send(embed=embed)

def setup(client):
  client.add_cog(kick(client))
