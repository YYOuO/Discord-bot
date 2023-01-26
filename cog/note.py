import discord
from discord.ext import tasks
import sqlite3
from set import cog_extension
import discord.utils
import datetime
from discord import app_commands


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

        @tasks.loop(minutes=5.0)
        async def nowtime():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                time = int(
                    datetime.datetime.today().strftime('%Y%m%d%H%M'))
                print(f'Now time: {time}')
                for a in self.note_list:
                    if self.time > a[2]:
                        self.clear_list.append(a)
                        await self.channel.send(f'Hey! {self.bot.get_user(int(self.note_list[a][0])).mention} {a[1]}')

    note = app_commands.Group(name="note", description="Notes commands")

    @note.command(name='list', description='List the notes')
    async def list(self, interaction: discord.Interaction):
        for a in self.note_list:
            await interaction.followup.send('|{:^35}|{:^16}|'.format('Message', 'Time'))
            await interaction.followup.send('|{:^35}|{:^16}|'.format(a[1], a[2]))
        print(self.note_list)

    @note.command(name='create', description='Create a new note')
    async def create(self, interaction: discord.Interaction, name: str, time: str):
        author = interaction.user.id
        if len(time) != 12:
            await interaction.response.send_message('Please follow the style yyyymmddhhmm ex. 202201190857')
            return 'Error!'
        if self.sql == False:
            if int(time):
                self.sql = True
                self.cur.execute(
                    "INSERT INTO `NOTE` (`USER`,`MESSAGE`,`TIMEE`) VALUES(?,?,?)", (author, name, time))
                self.con.commit()
            await interaction.response.send_message(f'**{name.upper()}** create success!', ephemeral=True)
            notes = self.cur.execute(
                "SELECT * FROM `NOTE` ORDER BY `TIMEE` DESC")
            self.note_list = notes.fetchall()
            self.sql = False
        else:
            await interaction.response.send_message('Wait for the last query finish!')

    @note.command(name='remove', description='Delete the note')
    async def remove(self, interaction: discord.Interaction, name: str):
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
            await interaction.response.send_message('Delete success!')
        else:
            await interaction.response.send_message('Wait for the last query finish!')

    @note.command(name='clear', description='Clear all expire notes')
    async def clear(self, interaction: discord.Interaction):
        author = interaction.user.id
        if not self.clear_list:
            await interaction.response.send_message('Nothing delete!')
        else:
            if self.sql == False:
                self.sql = True
                ll = []
                for a in self.clear_list:
                    ll.append((a[1], a[0]))
                    self.note_list.remove(a)
                self.cur.executemany(
                    "DELETE FROM NOTE WHERE MESSAGE=(?) AND USER=(?)", (ll, author))
                self.con.commit()
                self.sql = False
                await interaction.response.send_message('Remove all expired message!')
            else:
                await interaction.response.send_message('Wait for the last query finish!')


async def setup(bot):
    await bot.add_cog(Notes(bot))

    @bot.tree.context_menu(name='Remind me!')
    async def remind(interaction: discord.Interaction, messsage: discord.Message):
        await interaction.response.send_message('Got it ! ✅')
