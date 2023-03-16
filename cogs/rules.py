import discord 
from discord.ext import commands

class Rules(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Rules.py is ready!")

    @commands.command()
    async def rules(self, ctx):
        await ctx.send("https://docs.google.com/document/d/1C9wtkcws-csk4eRtAeWH54OxgIjIhQGj4DGpTKSR0qQ/edit?usp=sharing")

async def setup(client):
    await client.add_cog(Rules(client))