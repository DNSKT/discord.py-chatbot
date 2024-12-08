import discord
import ollama
from discord.ext import commands
import logging
from gtts import gTTS
import asyncio

messages = []

TOKEN = ''
intents = discord.Intents.all()
intents.members = True

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#------------------------------------------------------------------------------
def send(chat):
  messages.append(
    {
      'role': 'user',
      'content': chat,
    }
  )
  stream = ollama.chat(model='Model name', 
    messages=messages,
    stream=True,
  )

  response = ""
  for chunk in stream:
    part = chunk['message']['content']
    print(part, end='', flush=True)
    response = response + part

  messages.append(
    {
      'role': 'assistant',
      'content': response,
    }
  )
  print("")
  return response
#------------------------------------------------------------------------------

bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
@bot.command()
async def c(ctx,*,text):
    await ctx.send("Procesando...")
    chat = text
    if chat == "/exit":
        print("huh")
    elif len(chat) > 0:
        await ctx.send(send(chat))
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


async def play_audio(channel, audio):
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe path", source=audio))
    while vc.is_playing():
        await asyncio.sleep(.2)
    await vc.disconnect()

@bot.command()
async def tts(ctx,*,text):
    voice = ctx.author.voice.channel
    chat = text
    if chat == "/exit":
        print("huh")
    elif len(chat) > 0:
        #await ctx.send(send(chat))
        sound = gTTS(text=send(chat), lang='es', slow=False)
        sound.save('audio path')

    await play_audio(voice, "audio path")

bot.run(TOKEN)
