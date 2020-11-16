from discord.ext import commands, tasks
from datetime import datetime


class Main(commands.Cog):
    """Module housing most of the bot's main commands."""

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
        async with self.bot.session.head("https://addhq.xyz/api/status") as response:
            self.heartbeats[datetime.utcnow()] = response.status_code
    
    @commands.command(name="status")
    @commands.bot_has_permissions(embed_links=True, send_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def show_status(self, ctx: commands.Context, *, history: int = 5):
        """Shows up to 20 previous heartbeat pings."""
        history = min(min(20, history), len(self.heartbeats))
        beats = list(sorted(self.heartbeats.keys(), reverse=True))[:history]
        ret = f"Previous {history} heartbeats:\n"
        for key in beats:
            



setup = lambda bot: bot.add_cog(Main(bot))