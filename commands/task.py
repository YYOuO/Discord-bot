import keyword
from time import time
import discord
from discord.ext import commands
import asyncio
from set import cog_extension
import json
import datetime


class Task(cog_extension):
    # 初始化

    def __init__(self, bot):
       # 父類別初始化屬性(就是搬過來用)
        super().__init__(bot)

        async def interval():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(992786432030679070)
            while not self.bot.is_closed():
                await asyncio.sleep(1)
        self.bg = self.bot.loop.create_task(interval())


def setup(bot):
    bot.add_cog(Task(bot))
