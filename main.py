# requires:
# pip install discord.py
# pip install asyncio
# pip install bs4
# pip install imgurpython
# pip install youtube-dl
# put this (view raw) in the base directory:
#   https://github.com/Just-Some-Bots/MusicBot/blob/ea5e0daebd384ec8a14c9a585da399934e2a6252/libopus-0.x64.dll


import discord
import random
import asyncio
import requests
import config
from bs4 import BeautifulSoup
from discord.ext import commands
from os import listdir
from imgurpython import ImgurClient

client = ImgurClient(config.client_id, config.client_secret)

discord.opus.load_opus("libopus-0.x64.dll")

description = '''An Ok-ish bot'''

bot = commands.Bot(command_prefix='?', description=description)
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'music/%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    }
if not discord.opus.is_loaded():
    # libopus-0.x64.dll is required to run voice
    discord.opus.load_opus("libopus-0.x64.dll")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_disconnect():
    bot.connect()


@bot.command()
async def roll(dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


@bot.command(pass_context=True)
async def sb(ctx, sound, member: discord.Member = None):
    """Plays given Sound"""
    if member is None:
        member = ctx.message.author
    channel = member.voice.voice_channel
    voice = await bot.join_voice_channel(channel)
    player = voice.create_ffmpeg_player("soundboard/"+sound+'.mp3', options="-af volume=-25dB")
    player.start()
    while not player.is_done():
        await asyncio.sleep(0.002)
    await voice.disconnect()


@bot.command(pass_context=True)
async def sblist(ctx, member: discord.Member = None):
    """Sends PM with available soundboard sounds"""
    if member is None:
        member = ctx.message.author
    message= "Available Sounds: \n"
    for f in listdir("soundboard/"):
        message += (f.split(".")[0] + "\n")
    await bot.send_message(member, message)


@bot.command(pass_context=True)
async def sbadd(ctx, member: discord.Member = None):
    """Adds Sound to soundboard"""
    if member is None:
        member = ctx.message.author
    if member.server_permissions.administrator:
        if ctx.message.attachments:
            url = ctx.message.attachments[0]['url']
            local_filename = "soundboard/" + url.split('/')[-1]
            r = requests.get(url, stream=True)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            await bot.say("no attachments")
    else:
        await bot.add_reaction(ctx.message, "😞")


@bot.command(pass_context=True)
async def play(ctx, url, member: discord.Member = None):
    """Streams given YouTube or Soundcloud URLs"""
    if member is None:
        member = ctx.message.author
    game = discord.Game()
    game.name = "Ok-ish Music"
    await bot.change_presence(game=game)
    channel = member.voice.voice_channel
    await bot.add_reaction(ctx.message, "👌")
    if bot.voice_client_in(member.server):
        await bot.voice_client_in(member.server).disconnect()
    voice = await bot.join_voice_channel(channel)
    player = await voice.create_ytdl_player(url, ytdl_options=ydl_opts, options="-af volume=-20dB")
    player.start()
    while not player.is_done():
        await asyncio.sleep(0.002)
    await voice.disconnect()


@bot.command(pass_context=True)
async def monstercat(ctx, member: discord.Member = None):
    """Streams Monstercat from twitch"""
    if member is None:
        member = ctx.message.author
    game = discord.Game()
    game.name = "Monstercat"
    await bot.change_presence(game=game)
    channel = member.voice.voice_channel
    await bot.add_reaction(ctx.message, "👌")
    if bot.voice_client_in(member.server):
        await bot.voice_client_in(member.server).disconnect()
    voice = await bot.join_voice_channel(channel)
    player = await voice.create_ytdl_player('https://www.twitch.tv/monstercat', ytdl_options=ydl_opts, options="-af volume=-25dB")
    player.start()


@bot.command(pass_context=True)
async def leave(ctx, member: discord.Member = None):
    """Throws bot out of voice"""
    if member is None:
        member = ctx.message.author
    if bot.voice_client_in(member.server):
        await bot.voice_client_in(member.server).disconnect()
        await bot.change_presence(game=None)
    else:
        await bot.add_reaction(ctx.message, "😞")


@bot.command()
async def otter():
    """Sends random otter picture from Imgur"""
    items = client.gallery_tag("otter", sort='viral', page=0, window='year').items
    item = items[random.randint(0, 59)]
    while item.is_album:
        item = items[random.randint(0, 59)]
    if item.type == "image/gif":
        await bot.say(item.gifv)
    else:
        await bot.say(item.link)


@bot.command()
async def cat():
    """Sends random cat picture from Imgur"""
    items = client.gallery_tag("cat", sort='viral', page=0, window='year').items
    item = items[random.randint(0, 59)]
    while item.is_album:
        item = items[random.randint(0, 59)]
    if item.type == "image/gif":
        await bot.say(item.gifv)
    else:
        await bot.say(item.link)


@bot.command()
async def dog():
    """Sends random dog picture from Imgur"""
    items = client.gallery_tag("dog", sort='viral', page=0, window='year').items
    item = items[random.randint(0, 59)]
    while item.is_album:
        item = items[random.randint(0, 59)]
    if item.type == "image/gif":
        await bot.say(item.gifv)
    else:
        await bot.say(item.link)


@bot.command()
async def panda():
    """Sends random dog picture from Imgur"""
    items = client.gallery_tag("panda", sort='viral', page=0, window='year').items
    item = items[random.randint(0, 20)]
    while item.is_album:
        item = items[random.randint(0, 20)]
    if item.type == "image/gif":
        await bot.say(item.gifv)
    else:
        await bot.say(item.link)


@bot.command()
async def fse():
    """Shows current statusm0n status of the FSE Uni Duisburg-Essen"""
    data = requests.get("http://www.fse.uni-due.de/")
    soup = BeautifulSoup(data.content, "lxml")
    div = soup.find('span', id='statusm0nText')
    await bot.say(''.join(map(str, div.contents)))


@bot.command(pass_context=True)
async def delall(ctx, member: discord.Member = None):
    """Deletes all (up to 100) last Messages in current channel"""
    if member is None:
        member = ctx.message.author
    if member.server_permissions.manage_messages:
        await bot.purge_from(ctx.message.channel, limit=100)
        await bot.say("http://i.imgur.com/YkuLCd8.gifv")
    else:
        await bot.add_reaction(ctx.message, "😞")


@bot.command(pass_context=True)
async def delete(ctx, count, member: discord.Member = None):
    """Deletes a given number (up to 100) of the last Messages in current channel"""
    if member is None:
        member = ctx.message.author
    if int(count) > 100:
        count = 100
    if member.server_permissions.manage_messages:
        await bot.purge_from(ctx.message.channel, limit=int(count))
        await bot.say("PUFF und weg 💨")
    else:
        await bot.add_reaction(ctx.message, "😞")


bot.run(config.bottoken)
