import discord
from discord.ext import commands
from mcstatus import MinecraftServer
from datetime import datetime
from datetime import date
import asyncio
import os
from dotenv import load_dotenv
import pytz

load_dotenv()

bot = commands.Bot(command_prefix='pog ')

server_ip = os.getenv("SERVERIP")
server = MinecraftServer.lookup(server_ip) #poggerchair IP: 95.142.162.123:25565

async def request():
    while True:
        file1 = open("log.txt", "a")
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)
        today = date.today()
        status = server.status()
        tosay = "\nDate: {0} Time: {1} Players: {2} Latency: {3}".format(today, datetime_NY.strftime("%H:%M:%S"), status.players.online, status.latency)
        channel = bot.get_channel(841751991088971827) # REPLACE THE CHANNEL ID WITH YOURS 841751991088971827 876187825995919410
        await channel.edit(topic=str("{0}/20 players online | Last Edited at {1} EST".format(status.players.online, datetime_NY.strftime("%H:%M:%S"))), reason="Automatic Edit: Player Count Changed")
        file1.write(tosay)
        print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
        file1.close()
        await asyncio.sleep(300)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='poggerchair'))
    await request()

@bot.command()
async def ping(ctx):
    await ctx.send(":ping_pong: Pong!")

@bot.command()
async def playerCount(ctx):
        server = MinecraftServer.lookup(server_ip) #poggerchair IP: 95.142.162.123:25565
        status = server.status()
        await ctx.send("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
        print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))       

@bot.command()
async def players(ctx):
    server = MinecraftServer.lookup(server_ip) #poggerchair IP: 95.142.162.123:25565
    status = server.status()
    query = server.query()
    tz_NY = pytz.timezone('America/New_York') 
    datetime_NY = datetime.now(tz_NY)
    embed = discord.Embed(
        title = 'Poggerchair',
        description = "There is currently {0} player(s) online.".format(status.players.online),
        color = discord.Color.from_rgb(255, 103, 76))

    embed.set_footer(text='{0} | PogBot is a project by @SharkBaitBilly#5270'.format(datetime_NY.strftime("%H:%M:%S")))
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/876187825995919410/879860894258044948/pogbot.png')
    #embed.set_author(name='Bot Template',
    #icon_url='')
    embed.add_field(name='Player Count', value="{0}/20".format(status.players.online), inline=True)
    embed.add_field(name='Ping', value=status.latency, inline=True)
    if status.players.online > 0:
        embed.add_field(name='Player List', value="\n ".join(query.players.names), inline=False)
    await ctx.send(embed=embed)     

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
