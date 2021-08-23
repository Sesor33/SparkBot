import discord
import aiohttp
import asyncio
import json
from discord.ext import commands
from discord.utils import get

class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.steamSpyAPIURL = 'https://steamspy.com/api.php'
        self.steamCurrPlayerAPIURL = 'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v0001/?appid='


    @commands.command(brief="Gets the player numbers for a steam game based on AppID")
    async def playercount(self, ctx, appID : str):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.steamCurrPlayerAPIURL + appID) as request:
                if request.status == 200:
                    data = await request.json()
                    await ctx.send(f"Current players: {data['response']['player_count']}")
                else:
                    await ctx.send(f"Error, AppID: {appID} not found")

    @commands.command(brief="Gets the info for a steam game based on AppID", aliases=['gs', 'steamstats'])
    async def gamestats(self, ctx, appID : str):
        steamSpyRequestURL = f'{self.steamSpyAPIURL}?request=appdetails&appid={appID}'
        async with aiohttp.ClientSession() as session:
            async with session.get(self.steamCurrPlayerAPIURL + appID) as playerRequest:
                if playerRequest.status == 200:
                    playerCountData = await playerRequest.json()
                else:
                    await ctx.send(f"Error, AppID: {appID} not found")

            #TODO: Error handling outside of saying app not found
            async with session.get(steamSpyRequestURL) as request:
                if request.status == 200:
                    data = await request.json()

                    embed = discord.Embed(title = data['name'], description = f'AppID: {appID}', color = discord.Colour.blue())
                    embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Queried by {ctx.author.display_name}')
                    embed.set_thumbnail(url = f'http://cdn.akamai.steamstatic.com/steam/apps/{appID}/header.jpg')
                    embed.add_field(name = 'Developer', value = data['developer'] , inline = True)
                    embed.add_field(name = 'Publisher', value = data['publisher'] , inline = True)
                    embed.add_field(name = 'Price', value = f"${float(data['price'])/100:.2f}" , inline = True)
                    embed.add_field(name = 'Current Players', value = playerCountData['response']['player_count'], inline = True)
                    embed.add_field(name = 'Owners', value = data['owners'], inline = True)
                    embed.add_field(name = 'Store Link', value = f'http://store.steampowered.com/app/{appID}', inline = False)

                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Error, AppID: {appID} not found")


def setup(bot):
    bot.add_cog(Steam(bot))
