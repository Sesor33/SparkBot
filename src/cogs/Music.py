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

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo','connect'])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("\u180EYou are not connected to a voice channel")
            return
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send(f"\u180EJoined {channel}")

    @commands.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['dc','leave'])
    async def disconnect(self, ctx):
        await self.bot.voice_clients[0].disconnect()

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
        voice = get(self.bot.voice_clients, guild=ctx.guild)
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

        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio(songName))
        voice.volume = 100
        voice.is_playing()

    @commands.command(pass_context=True, brief="Repeats last song played", aliases=['playlast','again'])
    async def repeat(self, ctx):
        songName = f"{ctx.guild.id}.mp3"
        song_there = os.path.isfile(songName)
        try:
            if song_there:
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                voice.play(discord.FFmpegPCMAudio(songName))
                voice.volume = 100
                voice.is_playing()
        except:
            await ctx.send("\u180ENothing is in buffer, play a song first")
            return

    @commands.command(pass_context=True, brief="Pauses currently playing audio")
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()

    @commands.command(pass_context=True, brief="Stops currently playing audio")
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing() or voice.is_paused():
            voice.stop()

    @commands.command(pass_context=True, brief="Resumes paused audio",aliases=['unpause'])
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()

    @commands.command(pass_context=True, brief="Changes to volume",aliases=['vol','v'])
    async def volume(self, ctx, vol: int):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing() or voice.is_paused():
            voice.volume = vol

def setup(bot):
    bot.add_cog(Music(bot))
