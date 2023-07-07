import discord 
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("helpcommand.py is ready!")
    
    @commands.command()
    async def bothelp(self, ctx):
        help_embed = discord.Embed(title="Help Desk for Kaniving Bot", description="All commands for the bot", color=discord.Color.blurple())
        
        help_embed.set_author(name="Kaniving Bot")
        help_embed.add_field(name="$""clear", value="Deletes a specified number of messages", inline=False)
        help_embed.add_field(name="$""ping", value="Shares the latency of the bot", inline=False)
        help_embed.add_field(name="$""level", value="Checks the level of the desired user in the server", inline=False)
        help_embed.add_field(name="$""standings", value="Returns the document displaying the current standings for the league", inline=False)
        help_embed.add_field(name="$""rules", value="Returns the most current rules document for the current tournament/league", inline=False)
        help_embed.add_field(name="$user", value="Returns information about the desired user", inline=False)
        help_embed.add_field(name="Need Help?", value="Feel free to ping/message any of the mods", inline=False)
        
        help_embed.set_footer(text=f"Requested by {ctx.author.mention}.", icon_url=ctx.author.avatar)
        
        await ctx.send(embed = help_embed)        
       
        
    

  
async def setup(client):
    await client.add_cog(help(client))