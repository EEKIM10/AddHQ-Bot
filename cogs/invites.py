from discord.ext import commands
import discord
BASE = "https://addhq.xyz/api/v1"
AUTHHEAD = {"Authorization": os.getenv("ADDHQ_AUTH_TOKEN")}


class Invites(commands.Cog):
    """Commands related to managing invites via the bot rather than website"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(manage_server=True)
    @commands.bot_has_permissions(manage_server=True, manage_messages=True, embed_links=True)
    @commands.max_concurrency(1, commands.BucketType.guild, wait=False)
    async def create(self, ctx, code: str = None, invite: discord.Invite = None):
        msg = await ctx.send("Authenticating...")
        # async with self.bot.session.post(BASE+"/meta/auth", header={"UserID": ctx.author.id, **AUTHHEAD})
