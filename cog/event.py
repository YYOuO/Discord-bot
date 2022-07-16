import discord
from discord.ext import commands
import sqlite3
from set import cog_extension


class Main(cog_extension):
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == 'hi':
            await ctx.channel.send('幹嘛')


def setup(bot):
    bot.add_cog(Main(bot))
