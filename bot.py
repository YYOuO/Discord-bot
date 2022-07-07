import discord
from discord.ext import commands
# from discord.utils import get
import random
# 導入json
import json
import os
# 導入json檔
with open('setting.json', "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)
# 建置bot實體 以bot為代詞
# command_prefix=""前綴詞
bot = commands.Bot(command_prefix='/')


@bot.event  # event
async def on_ready():
    # 是否啟動
    print('BOT is online!!')
    channel = bot.get_channel(992786432030679070)
    await channel.send('Your bot is online!')
# 啟動bot


channel = bot.get_channel(jdata['channel'])


# ----------------------------------------------------------------------------------------------


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'commands.{extension}')
    await ctx.send('load {extension} .')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'commands.{extension}')
    await ctx.send('unload {extension} .')


@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'commands.{extension}')
    await ctx.send('reload {extension} .')


for file in os.listdir('./commands'):
    if file.endswith('.py'):
        bot.load_extension(f'commands.{file[:-3]}')


if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
