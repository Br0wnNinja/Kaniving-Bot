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
        channel_id = 1082531343747010560
        channel = self.client.get_channel(channel_id)
        await channel.send(f"Member joined: {member}")
        print("Member joined:", member)
        guild = member.guild
        invites_before = await guild.invites()
        await member.guild.chunk()
        invites_after = await guild.invites()
        
        for invite in invites_after:
            if invite.uses > 0 and invite not in invites_before:
                inviter = invite.inviter
                invite_code = invite.code
                invite_link = f"https://discord.gg/{invite_code}"
                await channel.send(f"Link Used: {invite_link}")

async def setup(client):
    await client.add_cog(Invite(client))
