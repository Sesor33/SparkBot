import discord
import youtube_dl
import os
import glob
import sys
import traceback
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
from secret import private as p
#Remember to pip discord.py[voice]

description = '''A discord bot to use in your gaming servers'''

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', description=description)

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(self, ctx.command, 'on_error'):
            return
        ignored = (commands.UserInputError)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.BadArgument):
            return await ctx.send('Memeber not found, please try again.')
        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send('Command not found')


#Voice

#@commands.command()
#async def join(self, ctx):
#    channel = ctx.message.author.voice.channel
#    vc = await channel.connect()

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print(client.user.id)
    print('All systems online!')

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")
try:
    client.run(p.botToken)
except Exception as e:
    print(f"Login error: {e}")
