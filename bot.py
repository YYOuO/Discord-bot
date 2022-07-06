import discord
from discord.ext import commands
import random
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
    channel = bot.get_channel(992786432030679070)
    await channel.send('Your bot is online!')
# 啟動bot


channel = bot.get_channel(jdata['channel'])


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 'hi':
        await message.channel.send('銃殺虫')
    await message.channel.send(message.content)


@bot.event
async def on_message(message):
    channel = bot.get_channel('992087111144579184')
    if message.author == bot.user:
        return
    if message.content[0] == '/':
        commandd = message.content[1:]
        print(commandd)
        await globals()[commandd](message)
        # await message.channel.send(message.content)
    else:
        await message.channel.send(message.content)
# ----------------------------------------------------------------------------------------------


@bot.command()  # command
async def picture(ctx):
    random_picture = random.choice(jdata['rickroll'])
    pic = discord.File(random_picture)
    await ctx.send(file=pic)


@bot.command()  # command
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}(ms)')


bot.run(jdata['TOKEN'])
