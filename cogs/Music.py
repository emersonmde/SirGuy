import re
import os
import youtube_dl
import discord
from discord.ext import commands


def delete_song(filename):
    os.remove(filename)
    print('Removed file {}'.format(filename))


class Music(commands.Cog):
    DEFAULT_VOLUME = 0.2

    def __init__(self, bot):
        self.bot = bot
        self.volume = {}

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""

        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send("You're not in a voice channel")
            return

        voice_client = ctx.voice_client
        if voice_client is not None and voice_client.is_connected():
            if voice_client.channel.id != voice_state.channel.id:
                await voice_client.move_to(voice_state.channel)
            return

        await voice_state.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        """Leaves a voice channel"""
        voice_client = ctx.voice_client
        if voice_client is None:
            await ctx.send('Not currently in a voice channel')
            return

        await voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, query: str):
        """
        Plays a song

        <query> must be a URL of a video or a search query
        """


        voice_client = ctx.voice_client
        if voice_client is None:
            await ctx.send('Not currently in a voice channel')
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '/tmp/sirguy_%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        await ctx.send('Searching YouTube for "{}"'.format(query))
        r = re.compile('^http.*//.*youtube.com.*$')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if r.match(query) is not None:
                search_term = query
            else:
                search_term = 'ytsearch1:{}'.format(query)
            search_results = ydl.extract_info(search_term, download=False)
            info = search_results['entries'][0] if 'entries' in search_results else search_results
            if info['duration'] > 600:
                await ctx.send('Error: video was longer then 10 minutes')
                return
            else:
                await ctx.send('Playing "{}"'.format(info['title']))
                ydl.download([info['id']])

        filename = '/tmp/sirguy_{}.mp3'.format(info['id'])

        voice_client.play(discord.FFmpegPCMAudio(filename), after=lambda e: delete_song(filename))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = self.DEFAULT_VOLUME

    @commands.command()
    async def pause(self, ctx):
        """Pauses a song that is playing"""
        voice_client = ctx.voice_client
        if voice_client is None:
            await ctx.send('Not currently in a voice channel')
            return

        if not voice_client.is_playing():
            await ctx.send("Not currently playing any songs")
            return

        await ctx.send('Pausing playback')
        voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """Resumes playback"""
        voice_client = ctx.voice_client
        if voice_client is None:
            await ctx.send('Not currently in a voice channel')
            return

        if not voice_client.is_paused():
            await ctx.send("Playback hasn't been paused")
            return

        await ctx.send('Resuming playback')
        voice_client.resume()

    @commands.command()
    async def stop(self, ctx):
        """Stops playback"""
        voice_client = ctx.voice_client
        if voice_client is None:
            await ctx.send('Not currently in a voice channel')
            return

        if not voice_client.is_playing():
            await ctx.send('Not currently playing any songs')
            return

        ctx.send('Stopped playback')
        voice_client.stop()

    @commands.command()
    async def volume(self, ctx, v: int):
        """Sets volume level (1-100)"""
        if v not in range(1, 101):
            await ctx.send("Volume level must be between 1 and 100")
            return

        voice_client = ctx.voice_client
        if voice_client is None:
            await ctx.send("Not currently in a voice channel")
            return

        if not isinstance(voice_client.source, discord.PCMVolumeTransformer):
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source)

        voice_client.source.volume = v / 100.0
        await ctx.send("Volume set to {}".format(v))
