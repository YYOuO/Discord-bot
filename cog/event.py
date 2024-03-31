import discord
from discord.ext import commands
from set import cog_extension
import discord.utils


class Event(cog_extension):
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == "hi":
            await ctx.channel.send("hello")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f"ERROR! {str(error)}")


async def setup(bot):
    await bot.add_cog(Event(bot))
