import discord
import json
from discord.ext import commands
from set import cog_extension
import time
from requests import get
import random
import sys
from discord import app_commands
sys.path.append('..')
with open('setting.json', "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class Cmds(cog_extension):

    @app_commands.command(name='ping', description='latnecy of bot')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Pong! {round(self.bot.latency*1000)} (ms)')

    @app_commands.command(name='add', description='add role')
    async def add(self, interaction: discord.Interaction):
        role = interaction.user.guild.get_role(993152574289104946)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f'{interaction.user.mention} get the permission {role}!')
        print(f'{interaction.user} get the role')

    @app_commands.command(name='draw', description='Take a draw for you')
    async def draw(self, interaction: discord.Interaction, quantity: int, choices: str):
        choices = choices.split()
        quantity = int(quantity)
        answer = ''
        for a in range(quantity):
            tmp = random.choice(choices)
            answer += tmp
            if a != quantity-1:
                answer += ' , '
        await interaction.response.send_message(f'就決定是你了！出來吧 {answer}！')

    @app_commands.command(name='dmme', description='create dm')
    async def dmme(self, interaction: discord.Interaction):
        dm = await self.bot.create_dm(user=discord.Object(id=interaction.user.id))
        await interaction.response.send_message("I've sent you a message !", ephemeral=True)
        await dm.send(content='what')


async def setup(bot):
    await bot.add_cog(Cmds(bot))
