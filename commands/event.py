import discord
from discord.ext import commands

from set import cog_extension


class Main(cog_extension):
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == 'hi':
            ctx.send('幹嘛')


def setup(bot):
    bot.add_cog(Main(bot))
