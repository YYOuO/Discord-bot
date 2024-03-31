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
        self.con = sqlite3.connect("note.db", timeout=8.0)
        self.cur = self.con.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS `NOTE`
            ( WHO INT,
            MESSAGE TEXT ,
            TIMEE TIMESTAMP,
            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
            );
            """
        )
        self.sql = False
        self.con.commit()
        self.clear_list = []
        self.time = 0
        self.total = self.cur.execute("SELECT count(*) FROM `NOTE`").fetchone()[0]
        self.nowtime.start()

    def cog_unload(self):
        self.nowtime.cancel()

    @tasks.loop(minutes=5.0)
    async def nowtime(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(992786432030679070)
        time = int(datetime.datetime.today().strftime("%Y%m%d%H%M"))
        print(f"Now time: {time}")
        notes = self.cur.execute("SELECT * FROM `NOTE` ORDER BY `TIMEE` DESC")
        for a in notes.fetchall():
            if time > int(a[2]):
                self.clear_list.append([a[0], a[1], a[3]])
                await channel.send(
                    f"Hey! {self.bot.get_user(int(a[0])).mention}  **{a[1]}** "
                )
        print("Time check End!")

    note = app_commands.Group(name="note", description="Notes commands")

    @note.command(name="list", description="List the notes")
    async def list(self, interaction: discord.Interaction):
        notes = self.cur.execute(
            "SELECT * FROM `NOTE` WHERE WHO=(?) ORDER BY `TIMEE` DESC",
            (interaction.user.id,),
        )
        text = "Total notes : " + str(self.total) + "\n"
        text += "|{:^10}|{:^40}|{:^20}|".format("ID", "Message", "Time") + "\n"
        for a in notes.fetchall():
            time = (
                str(a[2])[:4]
                + "-"
                + str(a[2])[4:6]
                + "-"
                + str(a[2])[6:8]
                + " "
                + str(a[2])[8:10]
                + ":"
                + str(a[2])[10:12]
            )
            text += "|{:^10}|{:^40}|{:^20}|".format(a[3], a[1], time) + "\n"
        await interaction.response.send_message(text, ephemeral=True)

    @note.command(name="create", description="Create a new note")
    async def create(
        self, interaction: discord.Interaction, name: str, time: str, who: discord.User
    ):
        if len(time) != 12:
            await interaction.response.send_message(
                "Please follow the format yyyymmddhhmm ex. 202201190857"
            )
            return "Error!"
        if self.sql:
            await interaction.response.send_message("Wait for the last query finish!")
        else:
            self.sql = True
            self.cur.execute(
                "INSERT INTO `NOTE` (`WHO`,`MESSAGE`,`TIMEE`) VALUES(?,?,?)",
                (
                    who.id,
                    name,
                    time,
                ),
            )
            self.con.commit()
            await interaction.response.send_message(
                f"**{name.upper()}** create .", ephemeral=True
            )
            self.sql = False

    @note.command(name="remove", description="Delete the note")
    async def remove(self, interaction: discord.Interaction, id: int):
        if self.sql:
            await interaction.response.send_message("Wait for the last query finish!")
        else:
            self.sql = True
            self.cur.execute("DELETE FROM NOTE WHERE ID=(?)", (id,))
            self.con.commit()
            self.sql = False
            self.clear_list.remove(
                next((element for element in self.clear_list if id in element), None)
            )
            await interaction.response.send_message("Delete.")

    @note.command(name="clear", description="Clear all expire notes")
    async def clear(self, interaction: discord.Interaction):
        if not self.clear_list:
            await interaction.response.send_message("Nothing delete!")
        else:
            if self.sql:
                await interaction.response.send_message(
                    "Wait for the last query finish!"
                )
            else:
                self.sql = True
                self.cur.executemany(
                    "DELETE FROM NOTE WHERE ID=(?) ",
                    (
                        (item[2],)
                        for item in [
                            element
                            for element in self.clear_list
                            if interaction.user.id in element
                        ]
                    ),
                )
                self.con.commit()
                self.clear_list = [
                    element
                    for element in self.clear_list
                    if interaction.user.id not in element
                ]
                self.sql = False
                await interaction.response.send_message("Remove all expired message!")


async def setup(bot):
    nn = Notes(bot=bot)
    await bot.add_cog(nn)

    class timeselect(Select):
        def __init__(
            self, message: discord.Message, interaction: discord.Interaction
        ) -> None:
            options = [discord.SelectOption(label=_) for _ in range(10, 120, 10)]
            self.message = message
            super().__init__(placeholder="Remind me _ minutes later", options=options)
            # super().__init__(placeholder="Who ?", options=users)

        async def callback(self, interaction: discord.Interaction):
            if nn.sql == False:
                nn.sql = True
                time = str(
                    (
                        datetime.datetime.today()
                        + datetime.timedelta(minutes=float(self.values[0]))
                    ).strftime("%Y%m%d%H%M")
                )
                print(datetime.datetime.now())
                print(time)
                nn.cur.execute(
                    "INSERT INTO `NOTE` (`USER`,`MESSAGE`,`TIMEE`) VALUES(?,?,?)",
                    (interaction.user.id, self.message.content, time),
                )
                nn.con.commit()
                nn.sql = False
                await interaction.response.edit_message(
                    content=f"**{self.message.content}** set! \n You've selete **{self.values[0]}** \n I'll remind you **{self.values[0]}** minutes later !",
                    view=None,
                )
            else:
                await interaction.response.send_message(
                    "Wait for the last query finish!"
                )

    @bot.tree.context_menu(name="Remind who!")
    async def remind(interaction: discord.Interaction, messsage: discord.Message):
        view = View()
        view.add_item(timeselect(messsage, interaction=interaction))
        await interaction.response.send_message("Got it ! ✅", view=view)
