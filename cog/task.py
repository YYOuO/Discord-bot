import discord
import datetime
import json
with open('./setting.json', 'r', encoding='UTF-8') as jfile:
    jdata = json.load(jfile)
from set import cog_extension
from discord.ext import commands
import asyncio
import sys
sys.path.append('..')


class Task(cog_extension):
    # 初始化

    def __init__(self, bot):
       # 父類別初始化屬性(就是搬過來用)
        super().__init__(bot)

        async def interval():
            await self.bot.wait_until_ready()
            guild = self.bot.get_guild(int(jdata['guild']))
            voice_channel = self.bot.get_channel(int(jdata['voice']))
            channel = self.bot.get_channel(int(jdata['channel']))
            role = guild.get_role(int(jdata['role']))
            while not self.bot.is_closed():
                print('task interval')

                for member in guild.members:
                    try:
                        usrvoice = member.voice.channel
                        if usrvoice != voice_channel:
                            print(member.voice.channel)
                            await member.remove_roles(role)
                            print(f'{member} role remove')
                        else:
                            await voice_channel.connect()
                    except:
                        await member.remove_roles(role)

                    await asyncio.sleep(5)

        self.bg = self.bot.loop.create_task(interval())


def setup(bot):
    bot.add_cog(Task(bot))
