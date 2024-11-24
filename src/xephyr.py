import discord
from discord.ext import commands
import yt_dlp as youtube_dl
from discord import FFmpegPCMAudio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioquality': 1,
    'outtmpl': 'downloads/%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'quiet': True,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

async def search_youtube(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extractaudio': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        url2 = info['url']
        return url2, info['title']

async def join_voice_channel(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()

async def play_audio(url, ctx):
    voice = ctx.voice_client
    if voice.is_playing():
        await ctx.send("Already playing audio.")
        return
    voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda e: print(f"Audio finished: {e}"))
    await ctx.send(f"Now playing: {url}")

@bot.command()
async def play(ctx, *, query):
    if ctx.author.voice:
        # If the user is in a voice channel, join that channel and play the music
        await join_voice_channel(ctx)
        url, title = await search_youtube(query)
        await play_audio(url, ctx)p
    else:
        await ctx.send("You need to join a voice channel first.")

@bot.command()
async def stop(ctx):
    voice = ctx.voice_client
    if voice:
        await voice.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("Not connected to a voice channel.")
# put your discord bot token here ↓
bot.run('YOUR_DISCORD_BOT_TOKEN')
