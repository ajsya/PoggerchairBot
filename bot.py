import discord
from discord.ext import commands
from mcstatus import MinecraftServer
from datetime import datetime
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
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)
        status = server.status()
        channel = bot.get_channel(841751991088971827) # REPLACE THE CHANNEL ID WITH YOURS
        await channel.edit(topic=str("{0}/20 players online | Last Edited at {1} EST".format(status.players.online, datetime_NY.strftime("%H:%M:%S"))), reason="Automatic Edit: Player Count Changed")
        print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
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

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
