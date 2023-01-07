import discord
from discord import app_commands
from mcstatus import JavaServer, BedrockServer
import string, base64, datetime

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False
    
    async def on_ready(self):
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 691656498698256405)) #to sync to all servers remove guilt argument (can take up to 24 hours to sync)
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name = "test", description = "testing", guild = discord.Object(id = 691656498698256405))
async def self(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}! This is a command for testing the functionality of slash commands!", ephemeral=True)

@tree.command(name = "server", description = "Minecraft Java Edition Server Status Lookup", guild = discord.Object(id = 691656498698256405))
async def self(interaction: discord.Interaction, address: str):
    try:
        server = JavaServer(address)
        status = server.status()
        
        chars = list(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation + ' ')
        motd = ''.join([i for i in status.description if i in chars])
        #print(motd)
        #print(status)

        thumbnail = status.favicon
        with open(f"thumbnails/{address}.png", "wb") as fh:
            img_data = thumbnail.replace("data:image/png;base64,", '')
            #print(img_data)
            img_data = bytes(img_data, 'utf-8')
            fh.write(base64.decodebytes(img_data))

        embed = discord.Embed(
            title = address,
            description = motd,
            color = discord.Color.from_rgb(255, 103, 76))
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text='PogBot is a project by @SharkBaitBilly#5270')
        file = discord.File(f'thumbnails/{address}.png', filename='thumbnail.png')
        embed.set_thumbnail(url=f"attachment://thumbnail.png")
        embed.set_author(name='PogBot', icon_url='https://cdn.discordapp.com/attachments/876187825995919410/879860894258044948/pogbot.png')
        embed.add_field(name='Player Count', value="{0}/{1}".format(status.players.online, status.players.max), inline=True)
        embed.add_field(name='Ping', value=str(round(status.latency, 2)) + " ms", inline=True)
        if status.players.online > 0:
            players = []
            for name in status.raw['players']['sample']:
                #print(name['name'])
                players.append(name['name'])
            #print(players)
            playersample=' '.join([str(item + "\n") for item in players])
            if not playersample:
                pass
            else:
                #playersample = ' '.join([str(item + "\n") for item in playersample])  
                embed.add_field(name='Player List', value=(str(playersample)), inline=False)
        embed.add_field(name='Server Version', value=status.version.name, inline=True)

        await interaction.response.send_message(file=file, embed=embed)
    except:
        await interaction.response.send_message("**UNKNOWN ERROR** The server requested server could not be located or did not respond. Did you mistype?", ephemeral=True)

client.run('NjExMjMzNTgwMjczODkzMzg2.XVQ1oQ.f_O64Lf5pcXij1S-V_Dx8EUZbAc')
