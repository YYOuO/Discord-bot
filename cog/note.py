import discord
from discord.ext import tasks
import sqlite3
from set import cog_extension
import discord.utils
import datetime
from discord import app_commands
from discord.ui import Select, View


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
            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
            );
            ''')
        self.sql = False
        self.con.commit()
        self.clear_list = []
        self.time = 0
        self.nowtime.start()

    @tasks.loop(minutes=5.0)
    async def nowtime(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(992786432030679070)
        time = int(datetime.datetime.today().strftime('%Y%m%d%H%M'))
        print(f'Now time: {time}')
        notes = self.cur.execute("SELECT * FROM `NOTE`  ORDER BY `TIMEE` DESC")
        for a in notes.fetchall():
            if time > int(a[2]):
                self.clear_list.append(a)
                await channel.send(f"Hey! {self.bot.get_user(int(a[0])).mention} Did you forget this -> **{a[1]}** ?")
        print('Time check End!')

    note = app_commands.Group(name="note", description="Notes commands")

    @note.command(name='list', description='List the notes')
    async def list(self, interaction: discord.Interaction):
        notes = self.cur.execute("SELECT * FROM `NOTE`  ORDER BY `TIMEE` DESC")
        text = '|{:^40}|{:^20}|'.format('Message', 'Time')+'\n'
        for a in notes.fetchall():
            test = str(a[2])[:4]+'-'+str(a[2])[4:6]+'-'+str(a[2])[6:8] + \
                ' '+str(a[2])[8:10]+':'+str(a[2])[10:12]
            text += '|{:^40}|{:^20}|'.format(a[1], test)+'\n'
        await interaction.response.send_message(text)

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
            for a in self.clear_list:
                if a[1] == name and a[0] == interaction.user.id:
                    self.clear_list.remove(a)
            await interaction.response.send_message('Delete success!')
        else:
            await interaction.response.send_message('Wait for the last query finish!')

    @note.command(name='clear', description='Clear all expire notes')
    async def clear(self, interaction: discord.Interaction):
        if not self.clear_list:
            await interaction.response.send_message('Nothing delete!')
        else:
            if self.sql == False:
                self.sql = True
                ll = []
                for a in self.clear_list:
                    ll.append((a[1], a[0]))
                    self.clear_list.remove(a)
                self.cur.executemany(
                    "DELETE FROM NOTE WHERE MESSAGE=(?) AND USER=(?)", ll)
                self.con.commit()
                self.sql = False
                await interaction.response.send_message('Remove all expired message!')
            else:
                await interaction.response.send_message('Wait for the last query finish!')


async def setup(bot):
    nn = Notes(bot=bot)
    await bot.add_cog(nn)

    class timeselect(Select):
        def __init__(self, message: discord.Message) -> None:
            options = [discord.SelectOption(label=_)
                       for _ in range(10, 120, 10)]
            self.message = message
            super().__init__(placeholder="Remind me _ minutes later", options=options)

        async def callback(self, interaction: discord.Interaction):
            if nn.sql == False:
                nn.sql = True
                time = str((datetime.datetime.today(
                )+datetime.timedelta(minutes=float(self.values[0]))).strftime('%Y%m%d%H%M'))
                print(datetime.datetime.now())
                print(time)
                nn.cur.execute(
                    "INSERT INTO `NOTE` (`USER`,`MESSAGE`,`TIMEE`) VALUES(?,?,?)", (interaction.user.id, self.message.content, time))
                nn.con.commit()
                nn.sql = False
            else:
                await interaction.response.send_message('Wait for the last query finish!')
            await interaction.response.edit_message(content=f"**{self.message.content}** set! \n You've selete **{self.values[0]}** \n I'll remind you **{self.values[0]}** minutes later !", view=None)

    @bot.tree.context_menu(name='Remind me!')
    async def remind(interaction: discord.Interaction, messsage: discord.Message):
        view = View()
        view.add_item(timeselect(messsage))
        await interaction.response.send_message('Got it ! ✅', view=view)
