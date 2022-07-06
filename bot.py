import discord
from discord.ext import commands
# from discord.utils import get
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


# @bot.event
# async def on_message(ctx):
#     if ctx.author == bot.user:
#         return
#     if ctx.content[0] == '/':
#         commandd = ctx.content[1:]
#         print(commandd)
#         await globals()[commandd](ctx)
#     if ctx.content == 'hi':
#         await ctx.channel.send('銃殺虫')

# ----------------------------------------------------------------------------------------------


@bot.command()  # command
async def picture(ctx):
    random_picture = random.choice(jdata['rickroll'])
    pic = discord.File(random_picture)
    await ctx.channel.send(file=pic)


@bot.command()  # command
async def ping(ctx):
    await ctx.channel.send(f'{round(bot.latency*1000)}(ms)')


# @bot.command(pass_context=True)
# This must be exactly the name of the appropriate role
# @commands.has_any_role("會員")
# if ctx.author.has_roles(993152574289104946):
#         await ctx.channel.send(f'{ctx.author.mention} you have already had the permission')
#     else:
@bot.command()
async def add(ctx):
    guild = bot.get_guild(866673958005506059)
    role = guild.get_role(993152574289104946)
    await ctx.author.add_roles(role)
    await ctx.channel.send(f'{ctx.author.mention} get the permission {role.mention}!')

bot.run(jdata['TOKEN'])
