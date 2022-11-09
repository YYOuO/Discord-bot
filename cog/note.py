import discord
from discord.ext import commands
import sqlite3
from set import cog_extension
import discord.utils


class Notes(cog_extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.con = sqlite3.connect('note.db')
        self.cur = self.con.cursor()
        # create table note
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS `NOTE` 
            ( USER INT , 
            MESSAGE TEXT , 
            TIMEE TIMESTAMP,
            PRIVATE BOOL);
            ''')
        self.con.commit()

    @commands.command()
    async def list(self, ctx):
        notes = self.cur.execute(
            "SELECT * FROM `NOTE`  ORDER BY `TIMEE` DESC")
        await ctx.send('Message       Time')
        await ctx.send('------------------')
        for a in notes.fetchall():
            await ctx.send(f'{a[1]}    {a[2]}')

    @commands.command()
    async def create(self, ctx, name, time, private):
        author = int(ctx.author.id)
        if len(time) != 8:
            await ctx.send('Please follow the style yyyymmdd ex. 20220222')
            return 'Error!'
        if private != '1' and private != '0':
            await ctx.send('Private variable must be 0 or 1 !')
            return 'Error!'
        self.cur.execute(
            "INSERT INTO `NOTE` (`USER`,`MESSAGE`,`TIMEE`,`PRIVATE`) VALUES(?,?,?,?)", (author, name, time, private))
        self.con.commit()
        await ctx.send(f'**{name}** create success!')

    @commands.command()
    async def delete(self, ctx, name):
        author = int(ctx.author.id)
        delete = self.cur.execute(
            "SELECT USER FROM NOTE WHERE MESSAGE=(?)", (name))
        self.con.commit()
        await ctx.send(type(delete))


async def setup(bot):
    await bot.add_cog(Notes(bot))
