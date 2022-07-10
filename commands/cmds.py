import discord
from discord.ext import commands
import json
with open('setting.json', "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)
from set import cog_extension
import random
import asyncio
import time


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

        channel = self.bot.get_channel(990988022143123476)
        await channel.connect()
        time.sleep(10)
        await ctx.author.remove_roles(role)
        await ctx.channel.send('超過時效！\n請重新申請書房卡！')

    @commands.command()  # command
    async def picture(self, ctx):
        random_picture = random.choice(jdata['rickroll'])
        pic = discord.File(random_picture)
        await ctx.channel.send(file=pic)
    start = 0

    @commands.command()
    async def go(self, ctx):
        self.start = self.start + time.time()
        await ctx.channel.send("start")

    @commands.command()
    async def stop(self, ctx):
        self.end = time.time()
        await ctx.channel.send(f'{self.end-self.start}(s)')


def setup(bot):
    bot.add_cog(Main(bot))
