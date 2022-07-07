import discord
from discord.ext import commands
import json
with open('setting.json', "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)
from set import cog_extension
import random


class Main(cog_extension):

    @commands.command()  # command
    async def ping(self, ctx):
        await ctx.channel.send(f'{round(self.bot.latency*1000)}(ms)')

    @commands.command()
    async def add(self, ctx):
        guild = self.bot.get_guild(866673958005506059)
        role = guild.get_role(993152574289104946)
        await ctx.author.add_roles(role)
        await ctx.channel.send(f'{ctx.author.mention} get the permission {role.mention}!')

    @commands.command()  # command
    async def picture(self, ctx):
        random_picture = random.choice(jdata['rickroll'])
        pic = discord.File(random_picture)
        await ctx.channel.send(file=pic)


def setup(bot):
    bot.add_cog(Main(bot))
