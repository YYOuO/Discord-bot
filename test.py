import discord
from discord.ext import commands
import random
import json

from commands.task import Task
bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    print('online')


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


@bot.command()
async def ping(message):
    await message.channel.send(f'{round(bot.latency*1000)}(ms)')

bot.run('OTkxMzYzMDUwNDI4OTYwODQ4.GaS3RB.Hk2vqvw2sqmH3VCbrG2c6dXCF9YR6Xn86pVPcU')
