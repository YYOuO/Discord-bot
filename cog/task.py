from todoist_api_python.api_async import TodoistAPIAsync
import discord
import json
with open('./setting.json', 'r', encoding='UTF-8') as jfile:
    jdata = json.load(jfile)
from set import cog_extension
from discord.ext import tasks
import asyncio
from TnfshNotifyApi import TnfshNotify
from requests import get


class Task(cog_extension):
    # 初始化
    def __init__(self, bot):
        # 父類別初始化屬性(就是搬過來用)
        super().__init__(bot)
        self.channel = self.bot.get_channel(992786432030679070)
        self.old_normal = []
        self.old_top = []
        self.checkrole.start()
        self.checknews.start()
        self.TOJcheck.start()

    def cog_unload(self):
        self.checkrole.cancel()
        self.checknews.cancel()
        self.TOJcheck.cancel()

    async def embedit(self, URL: str, TITLE: str, DESCRIPTION: str, GROUP: str, TOP: str, CHANNEL: str) -> None:
        url = 'https://www.tnfsh.tn.edu.tw/latestevent/'+URL
        embed = discord.Embed(
            title=TITLE, url=url, description=DESCRIPTION, color=0x6ad771)
        embed.set_author(
            name=GROUP, icon_url="https://upload.wikimedia.org/wikipedia/zh/thumb/e/e4/TNFSH_emblem.svg/1200px-TNFSH_emblem.svg.png")
        embed.set_thumbnail(
            url="https://www.tnfsh.tn.edu.tw/images/logo.png")
        embed.set_footer(text=TOP)
        await CHANNEL.send(embed=embed)

    @tasks.loop(minutes=20.0)
    async def checkrole(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(int(jdata['guild']))
        voice_channel = self.bot.get_channel(int(jdata['voice']))
        role = guild.get_role(int(jdata['role']))
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
    tnfsh = "https://www.tnfsh.tn.edu.tw/latestevent/Index.aspx?Parser=9,3,19"

    @tasks.loop(hours=1.0)
    async def checknews(self, tnfsh=tnfsh):
        await self.bot.wait_until_ready()
        tnfsh_notify = TnfshNotify(tnfsh)
        print('checknews start')
        normal_list = tnfsh_notify.getNormalList()
        top_list = tnfsh_notify.getPuttopList()
        kk, kk1, newtop, newnormal = False, False, 0, 0
        for a in range(10):
            try:
                if normal_list[a].getUrl() != self.old_normal[a].getUrl() and kk == False:
                    newnormal = a
                    kk = True
            except IndexError:
                pass
            try:
                if top_list[a].getUrl() != self.old_top[a].getUrl() and kk1 == False:
                    newtop = a
                    kk1 = True
            except IndexError:
                pass
        await asyncio.sleep(30)
        for a in top_list[newtop:]:
            await self.embedit(a.getUrl(), a.getText(), a.getClaimDate(), a.getClaimGroup(), "置頂！", self.channel)
        await asyncio.sleep(10)
        for a in normal_list[newnormal:]:
            await self.embedit(a.getUrl(), a.getText(), a.getClaimDate(), a.getClaimGroup(), "一般！", self.channel)
        self.old_normal = normal_list
        self.old_top = top_list
        print('Check finish!')

    # TOJ check
    @tasks.loop(minutes=30.0)
    async def TOJcheck(self):
        await self.bot.wait_until_ready()
        print('TOJcheck !')
        TOJ = get('https://toj.tfcis.org/oj/')
        self.channel = self.bot.get_channel(int(jdata['channel']))
        user = ['866673984731742239', '876805556122288138']
        if TOJ.status_code != 200:
            for usr in user:
                await self.channel.send(self.bot.get_user(int(usr)).mention)
            await self.channel.send(f'HTTP status CODE :{TOJ.status_code}')


async def setup(bot):
    await bot.add_cog(Task(bot))
