import discord
import aiohttp
import asyncio
import json
from discord.ext import commands
from discord.utils import get

class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Gets the avatar URL of a member")
    async def steamtest(self, ctx):
        await ctx.send("Steam module is online")

    @commands.command(brief="Gets the player numbers for a steam game based on AppID")
    async def playercount(self, ctx, appID : str):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v0001/?appid=' + appID) as request:
                if request.status == 200:
                    data = await request.json()
                    await ctx.send(f"Current players: {data['response']['player_count']}")
def setup(bot):
    bot.add_cog(Steam(bot))
