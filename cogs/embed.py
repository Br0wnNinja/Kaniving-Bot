import discord
from discord.ext import commands

class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Embed.py is ready!")
    
    @commands.command()
    async def embed(self, ctx):
        help_message = discord.Embed(title="Title", description="Descrption", color=discord.Color.purple())
        help_message.set_author(name=f"Requested by {ctx.author.mention}")
        help_message.set_thumbnail(url=ctx.Guild.icon)
        help_message.set_image(url=ctx.Guild.icon)
        help_message.add_field(name="Field Name", value="Value", inline="False")
        help_message.set_footer(text="Footer", icon_url=ctx.author.avatar)

        await ctx.send(embed=help_message)




async def setup(client):
    await client.add_cog(Embed(client))