import discord 
from discord.ext import commands

class userinfo(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("userinfo.py is ready!")
    
    @commands.command()
    async def user(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        elif member is not None:
            member = member
            
        info_embed = discord.Embed(title=f"{member.name}'s User Information", description="All information about this user", color=discord.Color.blurple())
        
        info_embed.set_thumbnail(url=member.avatar)
        info_embed.add_field(name="Name:", value=member.name, inline=False)
        info_embed.add_field(name="Nick Name:", value=member.display_name, inline=False)
        info_embed.add_field(name="Discriminator:", value=member.discriminator, inline=False)
        info_embed.add_field(name="ID:", value=member.id, inline=False)
        info_embed.add_field(name="Top Role:", value=member.top_role, inline=False)
        info_embed.add_field(name="Status:", value=member.status, inline=False)
        info_embed.add_field(name="Bot User:", value=member.bot, inline=False)
        info_embed.add_field(name="Account Created:", value=member.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"), inline=False)
        info_embed.add_field(name="Date Joined:", value=member.joined_at.__format__("%A, %d. %B %Y @ %H:%M:%S"), inline=False)
        
        info_embed.set_footer(text=f"Requested by {ctx.author.mention}.", icon_url=ctx.author.avatar)
        
        await ctx.send(embed = info_embed)     
       
        
    

  
async def setup(client):
    await client.add_cog(userinfo(client))