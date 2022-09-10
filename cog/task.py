import discord
import json
with open('./setting.json', 'r', encoding='UTF-8') as jfile:
    jdata = json.load(jfile)
from set import cog_extension
from discord.ext import commands
import asyncio
from TnfshNotifyApi import TnfshNotify


class Task(cog_extension):
    # 初始化
    async def embedit(self, URL, TITLE, DESCRIPTION, GROUP, TOP, CHANNEL):
        url = 'https://www.tnfsh.tn.edu.tw/latestevent/'+URL
        embed = discord.Embed(
            title=TITLE, url=url, description=DESCRIPTION, color=0x6ad771)
        embed.set_author(
            name=GROUP, icon_url="https://upload.wikimedia.org/wikipedia/zh/thumb/e/e4/TNFSH_emblem.svg/1200px-TNFSH_emblem.svg.png")
        embed.set_thumbnail(
            url="https://www.tnfsh.tn.edu.tw/images/logo.png")
        embed.set_footer(text=TOP)
        await CHANNEL.send(embed=embed)

    def __init__(self, bot):
       # 父類別初始化屬性(就是搬過來用)
        super().__init__(bot)
        # check role

        async def interval():
            await self.bot.wait_until_ready()
            guild = self.bot.get_guild(int(jdata['guild']))
            voice_channel = self.bot.get_channel(int(jdata['voice']))
            role = guild.get_role(int(jdata['role']))
            while not self.bot.is_closed():
                print('role check interval')
                for member in guild.members:
                    try:
                        usrvoice = member.voice.channel
                        if usrvoice != voice_channel:
                            await member.remove_roles(role)
                            print(f'{member} role remove')
                        else:
                            await voice_channel.connect()
                    except:
                        await member.remove_roles(role)
                    await asyncio.sleep(5)
        # chceknews
        self.old_normal = set()
        self.old_top = set()
        tnfsh = "https://www.tnfsh.tn.edu.tw/latestevent/Index.aspx?Parser=9,3,19"
        tnfsh_notify = TnfshNotify(tnfsh)

        async def checknews():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(992786432030679070)
            while not self.bot.is_closed():
                print('checknews start')
                normal_list = set(tnfsh_notify.getNormalList())
                top_list = set(tnfsh_notify.getPuttopList())
                nl = normal_list-self.old_normal
                tl = top_list-self.old_top
                await asyncio.sleep(5)
                for a in tl:
                    await self.embedit(a.getUrl(), a.getText(), a.getClaimDate(), a.getClaimGroup(), "置頂！", self.channel)
                for a in nl:
                    await self.embedit(a.getUrl(), a.getText(), a.getClaimDate(), a.getClaimGroup(), "一般！", self.channel)
                self.old_normal = normal_list
                self.old_top = top_list
                print('Check finish!')
                await asyncio.sleep(1800)

        self.bg = self.bot.loop.create_task(interval())
        self.check = self.bot.loop.create_task(checknews())


async def setup(bot):
    await bot.add_cog(Task(bot))
