import discord
from discord.ext import commands

async def create_embed(
    title="Command failed",
    description="You don't have permission to use this command",
    color=discord.Color.red(),
    **kwargs,
):
    embed = discord.Embed(title=title, description=description, color=color, **kwargs)
    return embed

async def handle_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            embed=await create_embed(
                description="You're on cooldown for {:.1f}s".format(error.retry_after)
            )
        )
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(embed=await create_embed(description='This command is disabled.'))
    else:
        await ctx.send(embed=await create_embed(description=error))