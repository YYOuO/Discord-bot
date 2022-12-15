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
            TIMEE TIMESTAMP);
            ''')
        self.sql = False
        self.con.commit()
        self.note_list = []
        self.clear_list = []
        self.time = 0
        notes = self.cur.execute(
            "SELECT * FROM `NOTE`  ORDER BY `TIMEE` DESC")
        for a in notes.fetchall():
            self.note_list.append(a)

        async def nowtime():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                self.time = int(
                    datetime.datetime.today().strftime('%Y%m%d%H%M'))
                print(f'Now time: {self.time}')
                for a in self.note_list:
                    if self.time > a[2]:
                        self.clear_list.append(a)
                        await self.channel.send(f'Hey! {self.bot.get_user(int(self.note_list[a][0])).mention} {a[1]}')
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
    async def create(self, ctx, name, time):
        author = int(ctx.author.id)
        if len(time) != 12:
            await ctx.send('Please follow the style yyyymmddhhmm ex. 202201190857')
            return 'Error!'
        if self.sql == False:
            if int(time):
                self.sql = True
                self.cur.execute(
                    "INSERT INTO `NOTE` (`USER`,`MESSAGE`,`TIMEE`) VALUES(?,?,?)", (author, name, time))
                self.con.commit()
            await ctx.send(f'**{name.upper()}** create success!', delete_after=5.0)
            notes = self.cur.execute(
                "SELECT * FROM `NOTE` ORDER BY `TIMEE` DESC")
            for a in notes.fetchall():
                self.note_list.append(a)
            self.sql = False
        else:
            ctx.send('Wait for the last query finish!')

    @commands.command()
    async def delete(self, ctx, name):
        if self.sql == False:
            self.sql = True
            self.cur.execute("DELETE FROM NOTE WHERE MESSAGE=(?)", (name,))
            self.con.commit()
            self.sql = False
            for a in self.note_list:
                if name in a:
                    self.note_list.remove(a)
                    if a in self.clear_list:
                        self.clear_list.remove(a)
            await ctx.send('Delete success!')
        else:
            ctx.send('Wait for the last query finish!')

    @commands.command()
    async def clear(self, ctx):
        author = int(ctx.author.id)
        if not self.clear_list:
            await ctx.send('Nothing delete!')
        else:
            if self.sql == False:
                self.sql = True
                ll = []
                for a in self.clear_list:
                    ll.append((a[1], a[0]))
                    self.note_list.remove(a)
                self.cur.executemany(
                    "DELETE FROM NOTE WHERE MESSAGE=(?) AND USER=(?)", (ll))
                self.con.commit()
                self.sql = False
                await ctx.send('Remove all expired message!')
            else:
                await ctx.send('Wait for the last query finish!')


async def setup(bot):
    await bot.add_cog(Notes(bot))
