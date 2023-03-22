import discord
from discord.ext import commands
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio

class TeamManagement(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect("team_data.db")
        self.c = self.conn.cursor()
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        self.client = gspread.authorize(credentials)
        self.sheet = self.client.open_by_key("1YXRxQyqH_FSCVCquI7rIOyOW1eIdYlf0nwL8c29odhw").sheet1  # Replace with your Google Spreadsheet name
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Team Managment is ready!")

    @commands.command()
    @commands.has_role("Staff Team")  # Requires user to have the "Staff Team" role to run the command
    async def create(self, ctx, *, team_name_members: str):
        """Create a new team with the specified name and add the specified members"""
        # Separate the team name from the mentioned teammates using a dash
        team_name, mentioned_members = team_name_members.split("-")
    
        # Create the role with the specified name
        role_name = team_name.replace(" ", " ")
        role = await ctx.guild.create_role(name=role_name)

        # Add the specified members to the role
        mentioned_members = mentioned_members.strip().split(" ")
        team_members = []
        for member in mentioned_members:
            try:
                member_obj = await commands.MemberConverter().convert(ctx, member)
                team_members.append(member_obj)
                await member_obj.add_roles(role)
            except commands.errors.MemberNotFound:
                pass

        # Add the first mentioned user to the Team Captain role
        team_captain_role = discord.utils.get(ctx.guild.roles, name="Team Captains")
        if team_captain_role is not None:
            for member in team_members:
                if member != ctx.author:
                    await member.add_roles(team_captain_role)
                    team_captain_name = member.display_name
                    break

            # Send a confirmation message
            user_mention = ctx.author
            user_name = ctx.author.display_name
            team_members_names = [member.display_name for member in team_members if member != ctx.author]
            team_members_name_str = ", ".join(team_members_names)
            member_mentions = " ".join(member.mention for member in team_members if member != ctx.author)
            team_captain = next((member for member in team_members if member != ctx.author), None)
            team_captain_mention = team_captain.mention if team_captain else "None"
            team_captain_real_name = team_captain.name if team_captain else "None"
            confirmation_message = f"Created team {team_name} with members {member_mentions}. Team Captain role given to {team_captain_mention}. By {user_mention.mention}!"
            await ctx.send(confirmation_message)
            
            # Write to SQLite database
            self.c.execute("INSERT INTO teams VALUES (?, ?, ?, ?)", (team_name, team_members_name_str, team_captain_name, user_name))
            self.conn.commit()
            
            
            row = [team_name, team_captain_real_name, team_members_name_str]
            self.sheet.append_row(row, value_input_option='RAW', insert_data_option='INSERT_ROWS', table_range='A1:B1')
            
        else:
            await ctx.send("Error: 'Team Captains' role not found.")
            
    @commands.command()
    async def list(self, ctx):
        """List all teams in the database"""
        self.c.execute("SELECT * FROM teams")
        teams = self.c.fetchall()
        if len(teams) == 0:
            await ctx.send("There are no teams in the database.")
        else:
            team_list = "List of teams:\n"
            for team in teams:
                team_list += f"{team[0]}: {team[1]} (Team Captain: {team[2]}) - Created by: {team[3]}\n"
            await ctx.send(team_list)
            
                
    @commands.command()
    @commands.has_role("Staff Team")
    async def deletefrom(self, ctx, *, team_name_members: str):
        """Delete a team with the specified name and remove the role from all members"""
        # Separate the team name from the mentioned teammates using a dash
        team_name, _ = team_name_members.split("-")
        role_name = team_name.replace(" ", " ")
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        # Remove the role from all members
        if role is not None:
            for member in ctx.guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
            await role.delete()

            # Delete the team from the database
            self.c.execute("DELETE FROM teams WHERE team_name=?", (team_name,))
            self.conn.commit()

            await ctx.send(f"Deleted team {team_name}.")
        else:
            await ctx.send(f"Error: Could not find a role named '{role_name}'.")

    @commands.command()
    @commands.has_role("Staff Team")
    async def deleteall(self, ctx):
        """Deletes all data from the team_data.db SQLite database"""

        self.c.execute("DELETE FROM teams")
        self.conn.commit()
        await ctx.send("All data has been deleted from the database.")
    
    
    
        

           
async def setup(client):
    await client.add_cog(TeamManagement(client))