import discord
from discord.ext import commands
from mcstatus import MinecraftServer
from datetime import datetime
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='pog ')

server_ip = os.getenv("SERVERIP")
server = MinecraftServer.lookup(server_ip) #poggerchair IP: 95.142.162.123:25565

async def request():
    while True:
        status = server.status()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        status = server.status()
        channel = bot.get_channel(841751991088971827) # REPLACE THE CHANNEL ID WITH YOURS
        await channel.edit(topic=str("{0}/20 players online | Last Edited at {1} EST".format(status.players.online, current_time)), reason="Automatic Edit: Player Count Changed")
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

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
