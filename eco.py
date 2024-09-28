import discord
import feedparser
from discord.ext import commands
import random
import openai
import os
from openai.types import ChatModel
from openai import OpenAI
import requests

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

cliente = OpenAI()

respuesta = cliente.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "¡Hola!"}
  ]
)


openai.api_key = 'org-emPQ9ZFy2nqzfAqqvGZEBnzn'

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola! Soy el bot {bot.user}!')

@bot.command()
async def causas(ctx):
    causas = ['La generación de energía', 'La deforestación',
              'La agricultura', 'El transporte', 'La industria',]
    # causaAleatoria = random.choice(causas)
    await ctx.send("Causas del cambio climatico")
    for causa in causas:
        await ctx.send(causa)

@bot.command()
async def reciclar(ctx):
    await ctx.send("Aquí tienes una guía rápida de reciclaje:\n"
                   "♻️ Papel y cartón: contenedor azul\n"
                   "♻️ Plásticos, latas y bricks: contenedor amarillo\n"
                   "♻️ Vidrio: contenedor verde\n"
                   "♻️ Orgánico: contenedor marrón\n"
                   "♻️ Resto: contenedor gris")
@bot.command()
async def clima_actual(ctx):
    try:
        response = requests.get("https://api.climateclock.world/v1/clock")
        data = response.json()
        co2_ppm = data['data']['modules']['co2']['value']
        temperature = data['data']['modules']['temperature']['value']
        await ctx.send(f"Datos actuales del cambio climático:\n"
                       f"CO2 en la atmósfera: {co2_ppm} ppm\n"
                       f"Aumento de temperatura global: {temperature}°C")
    except Exception as e:
        await ctx.send(f"Lo siento, no pude obtener los datos actuales: {str(e)}")

@bot.command()
async def eco_noticias(ctx):
    feed = feedparser.parse("http://feeds.bbci.co.uk/news/science_and_environment/rss.xml")
    embed = discord.Embed(title="Noticias sobre Medio Ambiente", color=0x00ff00)
    for entry in feed.entries[:5]:
        embed.add_field(name=entry.title, value=entry.link, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def pregunta(ctx, *, question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en cambio climático y medio ambiente."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message['content']
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"Lo siento, hubo un error al procesar tu pregunta: {str(e)}")

@bot.command()
async def consejo(ctx):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en cambio climático. Da un consejo breve y práctico para ayudar a combatir el cambio climático."},
                {"role": "user", "content": "Dame un consejo para combatir el cambio climático."}
            ]
        )
        advice = response.choices[0].message['content']
        await ctx.send(advice)
    except Exception as e:
        await ctx.send(f"Lo siento, hubo un error al generar el consejo: {str(e)}")


bot.run(TOKEN)
