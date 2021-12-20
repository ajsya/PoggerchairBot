import discord
from discord.ext import commands
from mcstatus import MinecraftServer
from datetime import datetime
from datetime import date
import asyncio
import os
from dotenv import load_dotenv
import pytz
from discord_buttons_plugin import *

load_dotenv()

bot = commands.Bot(command_prefix='pog ')

buttons = ButtonsClient(bot)

server_ip = os.getenv("SERVERIP")
channel_id = os.getenv("CHANNELID")
server = MinecraftServer.lookup(server_ip) #poggerchair IP: 95.142.162.123:25565

async def request():
    last_player_count = 0
    while True:
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)
        today = date.today()
        status = server.status()
        tosay = "\nDate: {0} Time: {1} Players: {2} Latency: {3}".format(today, datetime_NY.strftime("%H:%M:%S"), status.players.online, status.latency)
        channel = bot.get_channel(int(channel_id))
        if status.players.online != last_player_count:
            try:
                await channel.edit(topic=str("{0}/20 players online | Last Edited at {1} EST".format(status.players.online, datetime_NY.strftime("%H:%M:%S"))), reason="Automatic Edit: Player Count Changed")
                last_player_count = status.players.online
            except TimeoutError:
                await channel.send("Channel Topic could not be changed: Timeout Error")
            except:
                await channel.send("An unknown error occured while trying to update the channel's topic.")
        file1 = open("save.txt", "a")
        file1.write(tosay)
        #print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
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
    embed.add_field(name='Player Count', value="{0}/{1}".format(status.players.online, status.players.max), inline=True)
    embed.add_field(name='Ping', value=status.latency, inline=True)
    if status.players.online > 0:
        embed.add_field(name='Player List', value="\n ".join(query.players.names), inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def poggerchair(ctx):
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
    embed.add_field(name='Player Count', value="{0}/{1}".format(status.players.online, status.players.max), inline=True)
    embed.add_field(name='Ping', value=status.latency, inline=True)
    if status.players.online > 0:
        embed.add_field(name='Player List', value="\n ".join(query.players.names), inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def charecraft(ctx):
    server = MinecraftServer.lookup('charecraft.minehut.gg')
    status = server.status()
    tz_NY = pytz.timezone('America/New_York') 
    datetime_NY = datetime.now(tz_NY)
    embed = discord.Embed(
        title = 'charecraft',
        description = "There is currently {0} player(s) online.".format(status.players.online),
        color = discord.Color.from_rgb(255, 103, 76))

    embed.set_footer(text='{0} | PogBot is a project by @SharkBaitBilly#5270'.format(datetime_NY.strftime("%H:%M:%S")))
    embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_TCpL190sxwuMJWpm7eM1NUYYtnFQ9SyJn-0wVdV6Dzufad-rYasqlfmWoiudvdP1o0E&usqp=CAU')
    embed.add_field(name='Player Count', value="{0}/{1}".format(status.players.online, status.players.max), inline=True)
    embed.add_field(name='Ping', value=status.latency, inline=True)
    await ctx.send(embed=embed)          

@bot.command()
async def github(ctx):
    await buttons.send(
        content = "**View on Github**",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label = "Github",
                    style = ButtonType().Link,
                    url="https://github.com/ajsya/PoggerchairBot"
                )
            ])
        ]
    )      

@bot.command()
async def flag(ctx):
    flag = (":purple_square::purple_square::purple_square::purple_square::purple_square::purple_square::yellow_square::white_large_square::yellow_square::purple_square::purple_square::purple_square::purple_square::purple_square::purple_square:\n:purple_square::purple_square::purple_square::purple_square::purple_square::purple_square::yellow_square::white_large_square::yellow_square::purple_square::purple_square::purple_square::purple_square::purple_square::purple_square:\n:purple_square::purple_square::purple_square::purple_square::purple_square::yellow_square::yellow_square::white_large_square::yellow_square::yellow_square::purple_square::purple_square::purple_square::purple_square::purple_square:\n:yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::white_large_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square:\n:white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square::white_large_square:")
    flag2 = ("\n:yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::white_large_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square::yellow_square:\n:purple_square::purple_square::purple_square::purple_square::purple_square::yellow_square::yellow_square::white_large_square::yellow_square::yellow_square::purple_square::purple_square::purple_square::purple_square::purple_square:\n:purple_square::purple_square::purple_square::purple_square::purple_square::purple_square::yellow_square::white_large_square::yellow_square::purple_square::purple_square::purple_square::purple_square::purple_square::purple_square:\n:purple_square::purple_square::purple_square::purple_square::purple_square::purple_square::yellow_square::white_large_square::yellow_square::purple_square::purple_square::purple_square::purple_square::purple_square::purple_square:")
    await ctx.send(flag)
    await ctx.send(flag2)

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
