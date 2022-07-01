import discord
from discord.ext import commands
# 導入json
import json
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
# 啟動bot


channel = bot.get_channel(jdata['channel'])


@bot.command()  # command
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}(ms)')

bot.run(jdata['TOKEN'])
