import discord
from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hi(self, ctx):
        ctx.send("hai!!")


def setup(bot):
    bot.add_cog(BasicCommands(bot))
