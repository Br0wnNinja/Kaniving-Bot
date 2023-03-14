import os
import discord
import youtube_dl
import spotipy
import spotipy.util as util
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.ctx = None
        self.voice = None
        self.next_song = False
        self.song_queue = []

        self.SPOTIPY_CLIENT_ID = "Acb40bff23934ab2875d58b000d01f0d"
        self.SPOTIPY_CLIENT_SECRET = "774b7ca4b0fb438da051ebbcd2a69d5a"
        self.SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"
        self.SPOTIPY_USERNAME = "i6o94n1efrdog99b3lp09kve1"
        self.SPOTIPY_SCOPE = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing"

        self.client_credentials_manager = SpotifyClientCredentials(
            client_id=self.SPOTIPY_CLIENT_ID,
            client_secret=self.SPOTIPY_CLIENT_SECRET
        )
        self.spotify = spotipy.Spotify(
            client_credentials_manager=self.client_credentials_manager
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print("music.py is ready!")
        
        
    def play_song(self, song):
        if song.startswith("https://open.spotify.com/track/"):
            song_id = song.split("/")[-1]
            track = self.spotify.track(song_id)
            track_url = track["external_urls"]["spotify"]
            title = track["name"]
            artist = track["artists"][0]["name"]
            thumbnail = track["album"]["images"][0]["url"]
            duration = track["duration_ms"] // 1000
        else:
            with youtube_dl.YoutubeDL({}) as ydl:
                info = ydl.extract_info(song, download=False)
                title = info["title"]
                thumbnail = info["thumbnail"]
                duration = info["duration"]
                artist = info["uploader"]
                track_url = info["webpage_url"]

        embed = discord.Embed(
            title="Now Playing",
            description=f"[{title}]({track_url})",
            color=discord.Color.dark_red()
        )
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="Duration", value=self.format_duration(duration))
        embed.add_field(name="Artist", value=artist)

        self.ctx.voice_client.play(discord.FFmpegPCMAudio(song), after=lambda e: self.play_next())
        self.ctx.voice_client.source.volume = 0.5
        self.is_playing = True

        self.bot.loop.create_task(self.ctx.send(embed=embed))

    def play_next(self):
        if self.next_song:
            self.next_song = False
            if self.song_queue:
                self.play_song(self.song_queue.pop(0))
            else:
                self.is_playing = False
                self.bot.loop.create_task(self.ctx.send("Queue is empty, leaving voice channel."))
                self.bot.loop.create_task(self.leave_voice_channel())

    def format_duration(self, duration):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"

    @commands.command()
    async def play(self, ctx, *args):
        query = " ".join(args)
        if "open.spotify.com/track/" not in query:
            await ctx.send("Invalid query. Please provide a valid Spotify track URL.")
            return
        self.ctx = ctx

        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")

   
async def setup(client):
    await client.add_cog(Music(client))






