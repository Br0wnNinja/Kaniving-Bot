import discord
from discord.ext import commands
import asyncio
import youtube_dl

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voice = None
        self.song_queue = []

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @commands.Cog.listener()
    async def on_ready(self):
        print("music.py is ready!")
    
    def play_next(self):
        if len(self.song_queue) > 0:
            self.voice.play(discord.FFmpegPCMAudio(self.song_queue[0]['url'], **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            self.song_queue.pop(0)
        else:
            self.voice = None

    @commands.command()
    async def play(self, ctx, url):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return

        if self.voice is not None:
            await ctx.send("I am already playing a song")
            return

        self.voice = await ctx.author.voice.channel.connect()
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        self.song_queue.append({'url': url2, 'title': info['title']})

        if len(self.song_queue) == 1:
            self.play_next()

    @commands.command()
    async def skip(self, ctx):
        if self.voice is not None and self.voice.is_playing():
            self.voice.stop()
        else:
            await ctx.send("I am not currently playing anything")

    @commands.command()
    async def pause(self, ctx):
        if self.voice is not None and self.voice.is_playing():
            self.voice.pause()
        else:
            await ctx.send("I am not currently playing anything")

    @commands.command()
    async def resume(self, ctx):
        if self.voice is not None and self.voice.is_paused():
            self.voice.resume()
        else:
            await ctx.send("I am not currently paused")

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if self.voice is None:
            if ctx.author.voice:
                self.voice = await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif self.voice.is_playing():
            self.voice.stop()
            
    def cog_unload(self):
        if self.voice:
            self.voice.stop()
            self.song_queue.clear()
            asyncio.run_coroutine_threadsafe(self.voice.disconnect(), self.client.loop)

async def setup(client):
    await client.add_cog(Music(client))

