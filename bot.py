import discord
from discord.ext import commands

# 建置bot實體 以bot為代詞
# command_prefix=""前綴詞
bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    # 是否啟動
    print('BOT is online!!')
# 啟動bot


channel = bot.get_channel(992087111144579184)


@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}(ms)')

bot.run('OTkxMzYzMDUwNDI4OTYwODQ4.GaS3RB.Hk2vqvw2sqmH3VCbrG2c6dXCF9YR6Xn86pVPcU')
