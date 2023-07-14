import discord
from discord.ext import commands

class Ghost(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Ghost.py is ready!")
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.mentions:
            for mention in message.mentions:
                channel = message.channel
                await channel.send(f"{message.author.mention}, uh oh, I wouldn't ghost ping again if I were you :)")

async def setup(client):
    await client.add_cog(Ghost(client))