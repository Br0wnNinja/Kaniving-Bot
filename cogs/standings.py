import discord
from discord.ext import commands

class Standings(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Standings.py is ready!")

    @commands.command()
    async def standings(self, ctx):
        await ctx.send("Here is the document with the current standings:")
        await ctx.send("https://docs.google.com/spreadsheets/d/1Nz2XR53byxzZRQ3Xhaa97DksJM7gM_-FO3CkzwAcgdQ/edit#gid=0")
        
async def setup(client):
    await client.add_cog(Standings(client))
                
