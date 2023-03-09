import discord 
from discord.ext import commands

class Dm(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Dm.py is ready!")

    @commands.command()
    async def dm(self, ctx):
        await ctx.author.send("You have mail")
        
        

async def setup(client):
    await client.add_cog(Dm(client))