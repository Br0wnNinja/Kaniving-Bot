import discord 
from discord.ext import commands

class time(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("time.py is ready!")
    
    @commands.command()
    async def timezone(self, ctx):
        pass
        
        
        
    
async def setup(client):
    await client.add_cog(time(client))