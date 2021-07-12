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
#Remember to pip discord[voice]

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


class MainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Gets the avatar URL of a member")
    async def avatar(self, ctx, member : discord.Member):
        await ctx.send(f"{member.avatar_url}")

    @commands.command(brief="Test command, says who YOU are")
    async def whoami(self, ctx):
        await ctx.send('\u180EYou are ' + str(self, ctx.message.author))

    @commands.command(brief="Ping? Pong.")
    async def ping(self, ctx):
        await ctx.send('\u180Epong')

    @commands.command(brief="Shouts out your Twitch link")
    async def twitch(self, ctx):
        await ctx.send('\u180EFollow me on Twitch at https://www.twitch.tv/Tech_Coyote')

    @commands.command(brief="Gives info about SparkBot")
    async def info(self, ctx):
        version = 0.3
        embed = discord.Embed(title = "SparkBot")
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = "Version", value = f"{version}", inline = True)
        embed.add_field(name = "Info", value = f"Running on the Server: {ctx.message.author.guild.name}", inline = False)
        embed.add_field(name = "Stats", value = f"Discord API Latency: {(client.latency * 1000):.2f}ms", inline = False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Queried by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(brief="Gets info on a member")
    async def whois(self, ctx, member : discord.Member):
        embed = discord.Embed(title = member.name, description = member.mention, color = discord.Colour.blue())
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(name = "ID", value = member.id, inline = True)
        embed.add_field(name = "Role", value = member.top_role.mention, inline = True)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Queried by {ctx.author.display_name}" )
        await ctx.send(embed=embed)

    @commands.command(brief="Kicks member")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx,member : discord.Member,*,reason= "No reason given"):
        embed = discord.Embed(title = "Moderation", description = "Kicked "+member.name, color = discord.Colour.red())
        embed.add_field(name = "ID", value = member.id, inline = True)
        await member.send(f"You have been kicked for: {reason}")
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @commands.command(brief="Bans member")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx,member : discord.Member,*,reason= "No reason given"):
        embed = discord.Embed(title = "Moderation", description = "Banned "+member.name, color = discord.Colour.red())
        embed.add_field(name = "ID", value = member.id, inline = True)
        await member.send(f"You have been banned for: {reason}")
        await member.ban(reason=reason)
        await ctx.send(embed=embed)


#Voice

#@commands.command()
#async def join(self, ctx):
#    channel = ctx.message.author.voice.channel
#    vc = await channel.connect()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo','connect'])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("\u180EYou are not connected to a voice channel")
            return
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send(f"\u180EJoined {channel}")

    @commands.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['dc','leave'])
    async def disconnect(self, ctx):
        await client.voice_clients[0].disconnect()

    @commands.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl','p'])
    async def play(self, ctx, url: str):
        global vidTitle
        songName = f"{ctx.guild.id}.mp3"
        song_there = os.path.isfile(songName)
        try:
            if song_there:
                os.remove(songName)
        except PermissionError:
            await ctx.send("Wait for the current playing music end or use the 'stop' command")
            return
        await ctx.send("Getting everything ready, playing audio soon")
        print("Someone wants to play music let me get that ready for them...")
        voice = get(client.voice_clients, guild=ctx.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False) #Gets video info
            tempSec = info_dict["duration"] #Gets duration
            vidTitle = info_dict["title"]
            embed = discord.Embed(title = "Now Playing",
             description = info_dict["title"], color = discord.Colour.green()) #Embed with video info
            embed.add_field(name = "Uploader", value = info_dict["uploader"], inline = True)
            embed.add_field(name = "Duration", value = f"{int(tempSec/60):02d}:{tempSec%60:02d}", inline = True)
            embed.set_thumbnail(url = info_dict["thumbnails"][0]["url"]) #Gets the thumbnail
            embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Queried by {ctx.author.display_name}")
            await ctx.send(embed=embed)

        #for file in os.listdir("./"):
            #print(type(file))
            #if file.endswith(".mp3"):

        files = [file for file in os.listdir("./") if file.endswith(".mp3")]
        newest = max(files , key = os.path.getctime)
        os.rename(newest, f"{ctx.guild.id}.mp3") #Handles multi-server audio

        voice = get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(songName))
        voice.volume = 100
        voice.is_playing()

    @commands.command(pass_context=True, brief="Repeats last song played", aliases=['playlast','again'])
    async def repeat(self, ctx):
        songName = f"{ctx.guild.id}.mp3"
        song_there = os.path.isfile(songName)
        try:
            if song_there:
                voice = get(client.voice_clients, guild=ctx.guild)
                voice.play(discord.FFmpegPCMAudio(songName))
                voice.volume = 100
                voice.is_playing()
        except:
            await ctx.send("\u180ENothing is in buffer, play a song first")
            return

    @commands.command(pass_context=True, brief="Pauses currently playing audio")
    async def pause(self, ctx):
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()

    @commands.command(pass_context=True, brief="Stops currently playing audio")
    async def stop(self, ctx):
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing() or voice.is_paused():
            voice.stop()

    @commands.command(pass_context=True, brief="Resumes paused audio",aliases=['unpause'])
    async def resume(self, ctx):
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()

    @commands.command(pass_context=True, brief="Changes to volume",aliases=['vol','v'])
    async def volume(self, ctx, vol: int):
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing() or voice.is_paused():
            voice.volume = vol
#Reference commands

"""
@commands.command()
async def voicechan(self, ctx):
    channel = ctx.message.author.voice.channel
    await ctx.send(str(channel))
"""

"""
@commands.command()
async def test(self, ctx):
    user = ctx.message.author
    await ctx.send(str(user))
"""

"""
@commands.command()
async def square(self, ctx, num):
    val = int(num) * int(num)
    await ctx.send(str(num) + ' squared is ' + str(val))
"""

client.add_cog(CommandErrorHandler(client))
client.add_cog(MainCommands(client))
client.add_cog(Music(client))

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print(client.user.id)
    print('All systems online!')

client.run(p.botToken)
