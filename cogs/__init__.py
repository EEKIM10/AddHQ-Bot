from discord.ext import commands, tasks
from datetime import datetime
import discord


class Main(commands.Cog):
    """Module housing some of the bot's main commands."""

    def __init__(self, bot):
        self.bot = bot
        self.heartbeat.start()
        self.heartbeats = {}
        print("loaded cog.")
    
    def cog_unload(self):
        self.heatbeat.stop()
        print("Unloaded cog")

    @tasks.loop(minutes=2)
    async def heartbeat(self):
        try:
            async with self.bot.session.head("https://addhq.xyz/api/status") as response:
                self.heartbeats[datetime.utcnow()] = response.status
        except:
            self.heartbeats[datetime.utcnow()] = 503
    
    @commands.command(name="status")
    @commands.bot_has_permissions(embed_links=True, send_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def show_status(self, ctx: commands.Context, *, history: int = 5):
        """Shows up to 20 previous heartbeat pings."""
        history = min(min(20, history), len(self.heartbeats))
        beats = list(sorted(self.heartbeats.keys(), reverse=True))[:history]
        ret = f"Previous {history} heartbeats:\n"
        for key in beats:
            ret += f"{key.strftime('%X')} UTC+0: {self.heartbeats[key]}\n"
        return await ctx.send(
            embed=discord.Embed(
                description=ret,
                colour=discord.Colour.green()
            )
        )


setup = lambda bot: bot.add_cog(Main(bot))