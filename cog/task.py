import requests
from bs4 import BeautifulSoup
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

        async def checknews():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                print('url checked!')
                response = requests.get(jdata['tnfsh'])
                soup = BeautifulSoup(response.text, "html.parser")
                title_list = soup.find_all(
                    'span', {'class': 'list_word text_le'}, limit=10)
                date_list = soup.find_all(
                    'span', {'class': 'w15 hidden-xs'}, limit=10)
                channel = self.bot.get_channel(992786432030679070)
                for title in title_list:
                    url = title.select_one('a').get('href')
                    await channel.send(title.select_one('a').getText())
                    await channel.send(f'https://www.tnfsh.tn.edu.tw/latestevent/{url}')
                    print('finish!')
                await asyncio.sleep(3600)
        self.bg = self.bot.loop.create_task(interval())
        self.check = self.bot.loop.create_task(checknews())


def setup(bot):
    bot.add_cog(Task(bot))
