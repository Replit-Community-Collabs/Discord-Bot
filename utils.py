import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure
from gql.transport import exceptions as GQLExceptions
import json
from data import *

class BlacklistError(CheckFailure):
    """
    Raised when a blacklisted user writes a command
    """

    pass

async def check_user_in_blacklist(author):
    with open("users.json", "r") as f:
        users = json.load(f)
    if author in users["blacklist"]:
        return True
    else:
        return False

async def create_embed(

    title="Command failed",
    description="You don't have permission to use this command",
    color=discord.Color.red(),
    **kwargs,
):
    """Returns an embed"""
    embed = discord.Embed(title=title, description=description, color=color, **kwargs)
    return embed


async def handle_error(ctx, error, ephemeral=True):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(
            embed=await create_embed(
                description="You're on cooldown for {:.1f}s".format(error.retry_after),
                ephemeral=ephemeral,
            )
        )
    elif isinstance(error, commands.DisabledCommand):
        await ctx.reply(
            embed=await create_embed(description="This command is disabled."),
            ephemeral=ephemeral,
        )
    elif isinstance(error, GQLExceptions.TransportQueryError):
        data = json.dumps(
            error.message, sort_keys=True, indent=4, separators=(",", ": ")
        )
        await ctx.reply(
            embed=await create_embed(
                description=f"There was an error while attempting this query:\n```json\n{data}\n```"
            ),
            ephemeral=ephemeral
        )
    elif isinstance(error, BlacklistError):
        await ctx.reply(
            embed=await create_embed(description="You are blacklisted from this bot."),
            ephemeral=ephemeral,
        )
    else:
        await ctx.reply(
            embed=await create_embed(description=error), ephemeral=ephemeral
        )

def isDeveloper():
    """Returns True when the user has either the Developer or the New developer role"""
    async def predicate(ctx):
        roles = [r.id for r in ctx.author.roles]
        return ROLE_DEVELOPER in roles or ROLE_NEW_DEV in roles
    return commands.check(predicate)
    
    
