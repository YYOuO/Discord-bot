import os
import json
import discord
from discord.ext import commands
from discord import app_commands
# 導入json檔
with open('setting.json', "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class dcBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(command_prefix='.', intents=intent)
        self.extension = []
        for file in os.listdir('./cog'):
            if file.endswith('.py'):
                self.extension.append(f'cog.{file[:-3]}')

    async def setup_hook(self):
        for ext in self.extension:
            print(ext)
            await self.load_extension(ext)


# intents
intent = discord.Intents.default()
intent.members = True
intent.message_content = True

bot = dcBot(intent)


@bot.event  # event
async def on_ready():
    # load command tree to specify guild and sync
    bot.tree.copy_global_to(guild=discord.Object(id=866673958005506059))
    await bot.tree.sync(guild=discord.Object(id=866673958005506059))
    # online message
    print('BOT is online!!')
    channel = bot.get_channel(992786432030679070)
    await channel.send('Your bot is online!')

channel = bot.get_channel(jdata['channel'])


# ----------------------------------------------------------------------------------------------

@ bot.tree.command(name='load', description='Load extension')
async def load(interaction: discord.Interaction, extension: str):
    if str(interaction.user.id) != jdata['developer']:
        await interaction.response.send_message('You do not have the permission!')
        return
    await bot.load_extension(f'cog.{extension}')
    await interaction.response.send_message(f'load {extension} !')


@ bot.tree.command(name='unload', description='Unload extension')
async def unload(interaction: discord.Interaction, extension: str):
    if str(interaction.user.id) != jdata['developer']:
        await interaction.response.send_message('You do not have the permission!')
        return
    await bot.unload_extension(f'cog.{extension}')
    await interaction.response.send_message(f'Unload {extension} !')


@ bot.tree.command(name='reload', description='Reload extension')
async def reload(interaction: discord.Interaction, extension: str):
    if str(interaction.user.id) != jdata['developer']:
        await interaction.response.send_message('You do not have the permission!')
        return
    await bot.reload_extension(f'cog.{extension}')
    await interaction.response.send_message(f'Reload {extension} !')


if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
