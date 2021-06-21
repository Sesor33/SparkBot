import discord
import youtube_dl
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
from secret import private as p
#Remember to pip discord[voice]

client = commands.Bot(command_prefix='!')



@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print(client.user.id)
    print('All systems online!')

@client.command(brief="Gets the avatar URL of a member")
async def avatar(ctx, member : discord.Member):
    await ctx.send(f"{member.avatar_url}")

@client.command(brief="Test command, says who YOU are")
async def whoami(ctx):
    await ctx.send('You are ' + str(ctx.message.author))

@client.command(brief="Ping? Pong.")
async def ping(ctx):
    await ctx.send('pong')

@client.command(brief="Shouts out your Twitch link")
async def twitch(ctx):
    await ctx.send('Follow me on Twitch at https://www.twitch.tv/Tech_Coyote')

@client.command(brief="Gives info about SparkBot")
async def info(ctx):
    version = 0.3
    embed = discord.Embed(title = "SparkBot")
    embed.set_thumbnail(url = client.user.avatar_url)
    embed.add_field(name = "Version", value = f"{version}", inline = True)
    embed.add_field(name = "Info", value = f"Running on the Server: {ctx.message.author.guild.name}", inline = False)
    embed.add_field(name = "Stats", value = f"Discord API Latency: {(client.latency * 1000):.2f}ms", inline = False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Queried by {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command(brief="Gets info on a member")
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name, description = member.mention, color = discord.Colour.red())
    embed.set_thumbnail(url = member.avatar_url)
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.add_field(name = "Role", value = member.top_role.mention, inline = True)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Queried by {ctx.author.name}" )
    await ctx.send(embed=embed)



#Voice

#@client.command()
#async def join(ctx):
#    channel = ctx.message.author.voice.channel
#    vc = await channel.connect()

@client.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo','connect'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")

@client.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['dc','leave'])
async def disconnect(ctx):
    await client.voice_clients[0].disconnect()

@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl','p'])
async def play(ctx, url: str):
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
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, f"{ctx.guild.id}.mp3")
            print(songName)
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio(songName))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True, brief="Repeats last song played", aliases=['playlast','again'])
async def repeat(ctx):
    songName = f"{ctx.guild.id}.mp3"
    song_there = os.path.isfile(songName)
    try:
        if song_there:
            voice = get(client.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio(songName))
            voice.volume = 100
            voice.is_playing()
    except:
        await ctx.send("Nothing is in buffer, play a song first")
        return

@client.command(pass_context=True, brief="Pauses currently playing audio")
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()

@client.command(pass_context=True, brief="Stops currently playing audio")
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing() or voice.is_paused():
        voice.stop()

@client.command(pass_context=True, brief="Resumes paused audio",aliases=['unpause'])
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()

@client.command(pass_context=True, brief="Changes to volume",aliases=['vol','v'])
async def volume(ctx, vol: int):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing() or voice.is_paused():
        voice.volume = vol
#Reference commands

"""
@client.command()
async def voicechan(ctx):
    channel = ctx.message.author.voice.channel
    await ctx.send(str(channel))
"""

"""
@client.command()
async def test(ctx):
    user = ctx.message.author
    await ctx.send(str(user))
"""

"""
@client.command()
async def square(ctx, num):
    val = int(num) * int(num)
    await ctx.send(str(num) + ' squared is ' + str(val))
"""

client.run(p.botToken)
