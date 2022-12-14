import discord
from discord.ext import commands
import sqlite3
from set import cog_extension
import discord.utils
import datetime
import asyncio


class Notes(cog_extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.channel = self.bot.get_channel(992786432030679070)
        self.con = sqlite3.connect('note.db', timeout=8.0)
        self.cur = self.con.cursor()
        # create table note
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS `NOTE` 
            ( USER INT , 
            MESSAGE TEXT , 
            TIMEE TIMESTAMP,
            PRIVATE BOOL);
            ''')
        self.sql = False
        self.con.commit()
        self.note_list = []
        self.time = []
        notes = self.cur.execute(
            "SELECT * FROM `NOTE`  ORDER BY `TIMEE` DESC")
        for a in notes.fetchall():
            self.time.append(int(a[2]))
            self.note_list.append(a)

        async def nowtime():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                time = int(datetime.datetime.today().strftime('%Y%m%d%H%M'))
                print(time)
                self.time.sort()
                if time > self.time[0]:
                    await self.channel.send(f'Hey! {self.bot.get_user(int(self.note_list[0][0])).mention} {self.note_list[0][1]}')
                await asyncio.sleep(300)

        self.timesssss = self.bot.loop.create_task(nowtime())

    @commands.command()
    async def list(self, ctx):
        await ctx.send('Message       Time')
        await ctx.send('------------------')
        for a in self.note_list:
            await ctx.send(f'{a[1]}    {a[2]}')
        await ctx.send('------------------')

    @commands.command()
    async def create(self, ctx, name, time, private=0):
        author = int(ctx.author.id)
        if len(time) != 12:
            await ctx.send('Please follow the style yyyymmddhhmm ex. 202201190857')
            return 'Error!'
        if self.sql == False:
            if int(time):
                self.sql = True
                self.cur.execute(
                    "INSERT INTO `NOTE` (`USER`,`MESSAGE`,`TIMEE`,`PRIVATE`) VALUES(?,?,?,?)", (author, name, time, private))
                self.con.commit()
            await ctx.send(content='test', delete_after=5.0)
            await ctx.send(f'**{name}** create success!')
            notes = self.cur.execute(
                "SELECT * FROM `NOTE`  ORDER BY `TIMEE` DESC")
            for a in notes.fetchall():
                self.time.append(int(a[2]))
                self.note_list.append(a)
            self.sql = False
        else:
            ctx.send('Wait for the last query finish!')

    @commands.command()
    async def delete(self, ctx, name):
        author = int(ctx.author.id)
        dell = self.cur.execute(
            "SELECT * FROM NOTE WHERE MESSAGE=(?)", (name,))  # ',' make it a tuple
        dell = dell.fetchall()
        print(dell)
        if(dell[0][0] == '0'):
            if dell[0] == author:
                await ctx.send('you are author!')
            else:
                await ctx.send('private message!')
                return 'Falied!'
        else:
            if self.sql == False:
                self.sql = True
                self.cur.execute("DELETE FROM NOTE WHERE MESSAGE=(?)", (name,))
                self.con.commit()
                self.sql = False
                self.note_list.remove(name)
                await ctx.send('Delete success!')
            else:
                ctx.send('Wait for the last query finish!')


async def setup(bot):
    await bot.add_cog(Notes(bot))
