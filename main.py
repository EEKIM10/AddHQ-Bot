# Note: this will not be run on repl.it

import discord
import aiohttp
import os
from time import time_ns
import asyncio

from discord.ext import commands

MY_ID = 421698654189912064

bot = commands.Bot(
    commands.when_mentioned_or("-"),
    owner_id=MY_ID,
    activity=discord.Game("development mode"),
    status=discord.Status.dnd
)
async def fuck_deprecation_warning():
    timeout = aiohttp.ClientTimeout(total=20)
    bot.session = aiohttp.ClientSession(
        timeout=timeout
        )
bot.loop.run_until_complete(fuck_deprecation_warning())
bot.load_extension("cogs")
bot.load_extension("jishaku")

@bot.event
async def on_ready():
    print("Bot logged in as", bot.user.name, "with", len(bot.guilds), "guilds.")

@bot.command(name="ping")
@commands.cooldown(1, 5, commands.BucketType.channel)
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def ping(ctx: commands.Context):
    """Shows you the latency for the bot and API."""
    start_delay = time_ns()
    msg = await ctx.send(embed=discord.Embed(title="Pinging..."))
    delay = round((time_ns()-start_delay)/1e+6, 2)
    dapi = round(bot.latency*1000, 2)

    start_api = time_ns()
    async with bot.session.get("https://addhq.xyz/api/status") as response:
        aapi = round((time_ns()-start_api)/1e+6, 2)
        status = response.status
        text = await response.text()
        if text.startswith('"'): text=text[1:]
        if text.endswith('"'): text=text[:-1]
    return await msg.edit(
        embed=discord.Embed(
            title="Pong.",
            description=f"**Discord API Latency:** `{dapi}ms`\n"
                        f"**AddHQ API Latency:** `{aapi}ms` (status {status}, \"{text}\")\n"
                        f"**Message Delay:** `{delay}ms`",
            colour=discord.Colour.green()
        )
    )

@bot.command(aliases=['documentation'])
async def docs(ctx: commands.Context):
    """Returns the links to access the auto-generated documentation for addhq."""
    return await ctx.send("https://addhq.xyz/docs\nBase URL: https://addhq.xyz/api/")


bot.run(os.getenv("BOT_TOKEN"))
asyncio.get_event_loop().run_until_complete(bot.session.close())
