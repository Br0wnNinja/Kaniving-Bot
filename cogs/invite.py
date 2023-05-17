import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("invite.py is ready!")
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        invites = await guild.invites()
        
        for invite in invites:
            if invite.inviter and invite.uses > 0:
                inviter = invite.inviter
                invite_code = invite.code
                
            if invite.max_uses == 0:
                uses = "Unlimited"
            else:
                uses = invite.uses
                
                channel_id = 1082531343747010560
                channel = self.client.get_channel(channel_id)
                
                await channel.send(f"User {str(member)} joined from invite by {inviter.name}")
                await channel.send(f"Invite Code: {invite_code}")
                await channel.send(f"Invite Uses: {uses}")   
    
async def setup(client):
    await client.add_cog(Invite(client))