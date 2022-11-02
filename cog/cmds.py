import json
from tkinter.tix import Tree
from urllib import request
from discord.ext import commands
import discord
from set import cog_extension
import sqlite3
import time
from requests import get
import random
import sys
sys.path.append('..')
with open('setting.json', "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class Cmds(cog_extension):
    con = sqlite3.connect('study.db')

    @commands.command()  # command
    async def ping(self, ctx):
        await ctx.channel.send(f'{round(self.bot.latency*1000)}(ms)')

    @commands.command()
    async def add(self, ctx):
        guild = self.bot.get_guild(866673958005506059)
        role = guild.get_role(993152574289104946)
        await ctx.author.add_roles(role)
        await ctx.channel.send(f'{ctx.author.mention} get the permission {role.mention}!')
        print(f'{ctx.author} get the role')
        channel = self.bot.get_channel(990988022143123476)
        await channel.connect()

    @commands.command()  # command
    async def picture(self, ctx):
        random_picture = random.choice(jdata['rickroll'])
        pic = discord.File(random_picture)
        await ctx.channel.send(file=pic)
    start = 0

    @commands.command()
    async def go(self, ctx):
        self.start = self.start + time.time()
        await ctx.channel.send("start count")

    @commands.command()
    async def stop(self, ctx):
        self.end = time.time()
        await ctx.channel.send(f'totaltime:{self.end-self.start}(s)')

    @commands.command()
    async def draw(self, ctx, quantity, *choose):
        choose = list(choose)
        quantity = int(quantity)
        answer = []
        for a in range(quantity):
            tmp = random.choice(choose)
            choose.remove(tmp)
            answer.append(tmp)
        await ctx.send(f'就決定是你了！出來吧 {answer}！')

    @commands.command(pass_context=True)
    async def poke(self, ctx, member: discord.User, *, message=None):
        message = message or "lasfsdsflkasjdfdflsaasjdsf"
        await self.bot.send_message(member, message)

    @commands.command()
    async def dmm(self, ctx):
        dm = await self.bot.create_dm(ctx.author)
        await dm.send('whatever')


async def setup(bot):
    await bot.add_cog(Cmds(bot))
