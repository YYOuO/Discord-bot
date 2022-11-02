import os
import json
import discord
from discord.ext import commands
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

intent = discord.Intents.default()
intent.members = True
intent.message_content = True
bot = dcBot(intent)


@bot.event  # event
async def on_ready():
    # 是否啟動
    print('BOT is online!!')
    channel = bot.get_channel(992786432030679070)
    await channel.send('Your bot is online!')

channel = bot.get_channel(jdata['channel'])


# ----------------------------------------------------------------------------------------------

@bot.command()
async def load(ctx, extension):
    if str(ctx.message.author.id) != jdata['developer']:
        await ctx.send('You do not have the permission!')
        return
    await bot.load_extension(f'cog.{extension}')
    await ctx.send(f'load {extension} .')


@bot.command()
async def unload(ctx, extension):
    if str(ctx.message.author.id) != jdata['developer']:
        await ctx.send('You do not have the permission!')
        return
    await bot.unload_extension(f'cog.{extension}')
    await ctx.send(f'unload {extension} .')


@bot.command()
async def reload(ctx, extension):
    if str(ctx.message.author.id) != jdata['developer']:
        await ctx.send('You do not have the permission!')
        print(ctx.author.id)
        return
    await bot.reload_extension(f'cog.{extension}')
    await ctx.send(f'reload {extension} .')


if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
