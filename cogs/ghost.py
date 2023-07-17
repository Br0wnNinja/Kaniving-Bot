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
                emoji = discord.utils.get(message.guild.emojis, name="Nerd")
                bot_id = 1058305655343169666
                if mention.bot:
                    return
                if message.author.id == bot_id:
                    return
                if emoji:
                    await channel.send(f"{message.author.mention}, uh oh, I wouldn't ghost ping again if I were you {emoji}")
                else:
                    await channel.send(f"{message.author.mention}, uh oh, I wouldn't ghost ping again if I were you :)")

async def setup(client):
    await client.add_cog(Ghost(client))