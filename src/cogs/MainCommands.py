import discord
from discord.ext import commands
from discord.utils import get

class MainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Gets the avatar URL of a member')
    async def avatar(self, ctx, member : discord.Member):
        await ctx.send(f'{member.avatar_url}')

    @commands.command(brief='Test command, says who YOU are')
    async def whoami(self, ctx):
        await ctx.send('\u180EYou are ' + str(self, ctx.message.author))

    @commands.command(brief='Ping? Pong.')
    async def ping(self, ctx):
        await ctx.send('\u180Epong')

    @commands.command(brief='Shouts out your Twitch link')
    async def twitch(self, ctx):
        await ctx.send('\u180EFollow me on Twitch at https://www.twitch.tv/Tech_Coyote')

    @commands.command(brief='Gives info about SparkBot')
    async def info(self, ctx):
        version = 0.3
        embed = discord.Embed(title = 'SparkBot')
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.add_field(name = 'Version', value = f'{version}', inline = True)
        embed.add_field(name = 'Info', value = f'Running on the Server: {ctx.message.author.guild.name}', inline = False)
        embed.add_field(name = 'Stats', value = f'Discord API Latency: {(client.latency * 1000):.2f}ms', inline = False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Queried by {ctx.author.display_name}')
        await ctx.send(embed=embed)

    @commands.command(brief='Gets info on a member')
    async def whois(self, ctx, member : discord.Member):
        embed = discord.Embed(title = member.name, description = member.mention, color = discord.Colour.blue())
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(name = 'ID', value = member.id, inline = True)
        embed.add_field(name = 'Role', value = member.top_role.mention, inline = True)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f'Queried by {ctx.author.display_name}')
        await ctx.send(embed=embed)

    @commands.command(brief='Kicks member')
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx,member : discord.Member,*,reason= 'No reason given'):
        embed = discord.Embed(title = 'Moderation', description = 'Kicked '+member.name, color = discord.Colour.red())
        embed.add_field(name = 'ID', value = member.id, inline = True)
        await member.send(f'You have been kicked for: {reason}')
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @commands.command(brief='Bans member')
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx,member : discord.Member,*,reason= 'No reason given'):
        embed = discord.Embed(title = 'Moderation', description = 'Banned '+member.name, color = discord.Colour.red())
        embed.add_field(name = 'ID', value = member.id, inline = True)
        await member.send(f'You have been banned for: {reason}')
        await member.ban(reason=reason)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MainCommands(bot))
