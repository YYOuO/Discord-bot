from calendar import c
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="/")


@bot.event
async def on_message(ctx):
    channel = bot.get_channel('992087111144579184')
    if ctx.author == bot.user:
        return
    if ctx.content[0] == '/':
        commandd = ctx.content[1:]
        print('Function '+commandd+' execute!')
        await globals()[commandd](ctx)
        await ctx.channel.send(ctx.content)
    else:
        # await ctx.channel.send(ctx.content)
        await ctx.delete()
        await ctx.channel.send(f'{ctx.author.mention} says :'+ctx.content)


# @bot.command(pass_context=True)
# 不再傳遞上下文，而是將指定的文字作為參數傳遞給裝飾器
# This must be exactly the name of the appropriate role
# @commands.has_any_role("會員")
# if ctx.author.has_roles(993152574289104946):
#         await ctx.channel.send(f'{ctx.author.mention} you have already had the permission')
#     else:
