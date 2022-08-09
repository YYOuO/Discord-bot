import discord
from discord.ext import commands
import sqlite3
from set import cog_extension
import discord.utils


class Main(cog_extension):
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == 'hi':
            await ctx.channel.send('幹嘛')
        if ctx.content.lower() == "<:pepesad:873572961272090654>":
            await ctx.channel.send('衝殺虫')
    # @commands.Cog.listener()
    # async def emojis(self, ctx):

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f"ERROR! {str(error)}")


def setup(bot):
    bot.add_cog(Main(bot))
