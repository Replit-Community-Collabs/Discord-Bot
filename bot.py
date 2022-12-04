import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from utils import create_embed, handle_error

import os
import sys
import time
import random
import subprocess
import json

with open("config.json") as f:
    data = json.load(f)

FLOOP_CHANNELS, APPLICATION_CHANNEL, IDEA_CHANNEL = (
    data["CHANNELS"]["FLOOP_CHANNELS"],
    data["CHANNELS"]["APPLICATION_CHANNEL"],
    data["CHANNELS"]["IDEA_CHANNEL"],
)
DEVELOPER_ROLE = data["ROLES"]["DEVELOPER"]
NEWDEV_ROLE = data["ROLES"]["NEW_DEVELOPER"]
BLACKLISTED_USERS = data["BLACKLIST"]["USERS"]

load_dotenv()


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="r!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

    async def on_command_error(self, ctx, error):
        await handle_error(ctx, error, ephemeral=True)


bot = Bot()
client = bot


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


# idea thing
@bot.event
async def on_message(ctx):
    if ctx.author.bot:  # ignore bots
        return
    if ctx.channel.id == IDEA_CHANNEL:  # check if the message is in the idea channel
        if ctx.content.startswith("."):
            return  # allow users to comment things if they put a . in front of their message
        await ctx.delete()
        embed = await create_embed(
            title=f"New idea by **{ctx.author.name}**",
            description=ctx.content,
        )
        embed.set_footer(text="Please vote on this idea!")
        msg = await ctx.channel.send(embed=embed)
        crossM = await bot.get_emoji(data["EMOTES"]["CHECKMARK"])  # get the emotes
        checkM = await bot.get_emoji(data["EMOTES"]["CROSSMARK"])
        await msg.add_reaction(crossM)  # add the reactions
        await msg.add_reaction("😐")
        await msg.add_reaction(checkM)

    await bot.process_commands(ctx)  # process commands


# !TODO - Write a custom check to check for either the developer role or the new developer role


@bot.hybrid_command(
    name="restart", with_app_command=True, description="Restart the bot"
)
@commands.has_role(DEVELOPER_ROLE)
async def restart(ctx):
    await ctx.defer(ephemeral=False)
    if not ctx.author.guild_permissions.administrator:
        await ctx.reply(embed=await create_embed())
        return
    if ctx.author.id in BLACKLISTED_USERS:
        await ctx.reply("No, you have been blacklisted from using this command.")
        return
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
    blocked = False
    if user.id == 915670836357247006:
        await ctx.reply("No lol.")
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
                if blocked == False:
                    await ctx.author.send(
                        embed=await create_embed(
                            title="Oh no!",
                            description=f"{user.mention} has blocked me. I am unable to floop them in DMs and have resorted to channels",
                        )
                    )
                    blocked = True
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


@bot.hybrid_command(
    with_app_command=True,
    name="exec_gql",
    description="Execute a GraphQL request.",
)
@commands.has_role(DEVELOPER_ROLE)
async def exec_gql(
    ctx,
    *,
    query: str,
    endpoint: str = "https://9abe713f-fe43-4eaf-9e93-ccaf2807f9d4.id.repl.co/graphql",
):
    await ctx.defer(ephemeral=False)
    transport = AIOHTTPTransport(url=endpoint)
    async with Client(transport=transport) as client:
        context = gql(query)
        data = await client.execute(context)
        return await ctx.reply(
            embed=await create_embed(
                title="Response",
                description=f"""```json
{json.dumps(data, sort_keys=True, indent=4, separators=(",", ": "))}
```""",
            )
        )


@bot.hybrid_command(
    with_app_command=True,
    name="list_all_repls",
    description="List all repls in the database",
)
@commands.has_role(DEVELOPER_ROLE)
async def list_all_repls(ctx):
    await ctx.defer(ephemeral=False)
    transport = AIOHTTPTransport(
        url="https://9abe713f-fe43-4eaf-9e93-ccaf2807f9d4.id.repl.co/graphql"
    )
    async with Client(transport=transport) as client:
        query = gql(
            """
    {
    domains {
        name
        owner
    }
    }
    """
        )
        data = await client.execute(query)
        return await ctx.reply(
            embed=await create_embed(
                title="Data",
                description=f"""```json
{json.dumps(data['domains'], sort_keys=True, indent=4, separators=(",", ": "))}
```""",
            )
        )


@bot.hybrid_group(
    with_app_command=True, name="application", description="Apply to be a RCC dev!"
)
async def applications(ctx):
    # This is never used as a slash command - so this would be a fallback command.
    await ctx.reply(
        "Want to apply to be an RCC dev? Use the `</application apply:1046497374626918541>` command!"
    )


@applications.command(name="apply", description="Apply to be an RCC dev!")
async def apply(ctx, *, application: str, replit_username: str, github_username: str):
    await ctx.defer(ephemeral=True)
    channel = bot.get_channel(APPLICATION_CHANNEL)
    embed = await create_embed(
        title=f"New Application",
        description=f"New application to be an RCC dev by {ctx.author.mention}!",
        color=discord.Color.yellow(),
    )
    embed.add_field(name="Application", value=application)
    embed.add_field(name="Replit", value=f"https://replit.com/@{replit_username}")
    embed.add_field(name="GitHub", value=f"https://github.com/{github_username}")
    embed.set_footer(
        text=f"Application by {ctx.author.name}#{ctx.author.discriminator}"
    )

    msg = await channel.send(embed=embed)
    # content=f"<@{ctx.author.id}>",

    thread = await msg.create_thread(name=ctx.author.name, reason="Application")
    await thread.send(
        "Hey! Thanks for applying to be an RCC Dev. We'll get back to you as soon as possible!"
    )
    with open("data/applications.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open("data/applications.json", "w", encoding="utf-8") as f:
        data[str(thread.id)] = {
            "applicant": ctx.author.id,
            "name": f"{ctx.author.name}#{ctx.author.discriminator}",
            "application": application,
            "replit": replit_username,
            "github": github_username,
            "votes": 0,
            "voters": [],
        }
        json.dump(data, f)
    await ctx.reply(f"Your application has been created! View it at {thread.mention}!")


@applications.command(name="vote", description="...")
@commands.has_role(DEVELOPER_ROLE)
async def vote(ctx):
    await ctx.defer(ephemeral=True)
    if ctx.channel.type != discord.ChannelType.public_thread:
        return await ctx.reply("You can only use this command in a thread.")

    starter_message = ctx.channel.starter_message

    with open("data/applications.json", "r") as f:
        applications_data = json.load(f)

    if (
        starter_message.author.id == bot.user.id
        and starter_message.channel.id == 1046479555839410206
    ):
        embed = starter_message.embeds[0].copy()

        votes = int(embed.footer.split("|")[1]) + 1

        embed.set_footer(text=f"⬆️ {votes} votes | {votes}")

        starter_message.edit(embed=embed)
        await ctx.reply("Your vote has been cast!")
    else:
        return await ctx.reply("This doesn't seem to be a valid application...")


@bot.hybrid_command(with_app_command=True, name="exec", description="Execute a command")
@commands.has_role(DEVELOPER_ROLE)
async def exec(ctx, *, command: str):
    await ctx.defer(ephemeral=False)
    response = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=10
    )
    if response.returncode == 0:
        return await ctx.reply(
            embed=await create_embed(
                title=f"Output for {command}",
                description=f"""```bash
{response.stdout}
```""",
            )
        )
    else:
        return await ctx.reply(
            embed=await create_embed(
                title=f"Oops!", description="Sorry, something went wrong!"
            )
        )


try:
    bot.run(os.environ["BOT_TOKEN"])
except Exception as e:
    print(f"ERROR WITH LOGGING IN: {e}")
