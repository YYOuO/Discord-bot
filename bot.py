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
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix='/')


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
    if str(ctx.message.author.id) != jdata['developer']:
        await ctx.send('You do not have the permission!')
        return
    bot.load_extension(f'cog.{extension}')
    await ctx.send(f'load {extension} .')


@bot.command()
async def unload(ctx, extension):
    if str(ctx.message.author.id) != jdata['developer']:
        await ctx.send('You do not have the permission!')
        return
    bot.unload_extension(f'cog.{extension}')
    await ctx.send(f'unload {extension} .')


@bot.command()
async def reload(ctx, extension):
    if str(ctx.message.author.id) != jdata['developer']:
        await ctx.send('You do not have the permission!')
        print(ctx.author.id)
        return
    bot.reload_extension(f'cog.{extension}')
    await ctx.send(f'reload {extension} .')


for file in os.listdir('./cog'):
    if file.endswith('.py'):
        print(file[:-3])
        bot.load_extension(f'cog.{file[:-3]}')


if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
