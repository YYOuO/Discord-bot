import discord
from discord.ext import commands
import sqlite3
from set import cog_extension
import discord.utils


class Event(cog_extension):
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == 'hi':
            await ctx.channel.send('幹嘛')
        if ctx.content.lower() == "<:pepesad:873572961272090654>":
            await ctx.channel.send('衝三小')
            await ctx.channel.send('<:eatgold:987356435610476635>')
        if ctx.content.lower() == "<:pepehappy:868860098708119593>":
            await ctx.channel.send('笑死幹')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f"ERROR! {str(error)}")


async def setup(bot):
    await bot.add_cog(Event(bot))
