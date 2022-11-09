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
            TIMEE TIMESTAMP  );
            ''')
        self.con.commit()

    @commands.command()
    async def create(self, ctx, name, time):
        author = int(ctx.author.id)
        if len(time) != 8:
            await ctx.send('Please follow the style yyyymmdd ex. 20220222')
            return 'Error!'
        self.cur.execute(
            "INSERT INTO `NOTE` (`USER`,`MESSAGE`,`TIMEE`) VALUES(?,?,?)", (author, name, time))
        self.con.commit()
        await ctx.send(f'**{name}** create success!')

    @commands.command()
    async def delete(self, ctx, name):
        operator = int(ctx.author.id)

    @commands.command()
    async def list(self, ctx):
        self.cur.execute()


async def setup(bot):
    await bot.add_cog(Notes(bot))
