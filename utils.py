import discord
from discord.ext import commands
from gql.transport import exceptions as GQLExceptions
import json


async def create_embed(
    title="Command failed",
    description="You don't have permission to use this command",
    color=discord.Color.red(),
    **kwargs,
):
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
    else:
        await ctx.reply(
            embed=await create_embed(description=error), ephemeral=ephemeral
        )
