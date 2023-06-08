import discord
from discord import permissions
from discord.ext import commands
from discord.utils import get
from bot import client, t
import requests
import asyncio


class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, arg = None):
        if arg is None:
            print(f'{ctx.author} enter help command')
            emb = discord.Embed(title = 'Команды', color = discord.Color.orange())
            emb.add_field(name = 'Admin', value = t['PREFIX'] + '`help admin`', inline = False)
            emb.add_field(name = 'User', value = t['PREFIX'] + '`help user`', inline = False)

        elif arg == 'admin':
            emb = discord.Embed(title = 'Команды', color = discord.Color.orange())
            emb.add_field(name = t['PREFIX'] + '`mute [@ник] [время] [причина]`', value = 'Заглушает человека', inline = False)
            emb.add_field(name = t['PREFIX'] + '`unmute [@ник]`', value = 'Разглушает человека', inline = False)
            emb.add_field(name = t['PREFIX'] + '`warn [@ник] [причина]`', value = 'Выдаёт предупреждение человеку', inline = False)
            emb.add_field(name = t['PREFIX'] + '`ban [@ник] [причина]`', value = 'Блокирует человека', inline = False)
            emb.add_field(name = t['PREFIX'] + '`unban [@ник]`', value = 'Убирает блокировку с человека', inline = False)
            emb.add_field(name = t['PREFIX'] + '`send [id канала] [текст]`', value = 'Отправляет сообщение в канал', inline = False)
            emb.add_field(name = t['PREFIX'] + '`embed [id канала] [текст]`', value = 'Отправляет embed в канал', inline = False)
            emb.add_field(name = t['PREFIX'] + '`clear [кол-во сообщений]`', value = 'Очистка чата', inline = False)
        
        elif arg == 'user':
            emb = discord.Embed(title = 'Команды', color = discord.Color.orange())
            emb.add_field(name = t['PREFIX'] + '`weather [город]`', value = 'Узнать погоду', inline = False)

        emb.set_author(name = "Sandwich Community", icon_url = 'https://cdn.discordapp.com/attachments/968956363558494218/968979654042071120/sandwich_art.jpg')
        await ctx.reply(embed = emb)

    @commands.command()
    async def weather(self, ctx, *, city: str):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = city
        complete_url = base_url + "appid=" + t['api_key'] + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel
        if x["cod"] != "404":
            async with channel.typing():
                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                weather_description = z[0]["description"]
                emb = discord.Embed(title=f"Погода в городе {city_name}", color = discord.Color.orange(), timestamp=ctx.message.created_at)
                emb.add_field(name="Описание", value=f"**{weather_description}**", inline=False)
                emb.add_field(name="Температура(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
                emb.add_field(name="Влажность(%)", value=f"**{current_humidity}%**", inline=False)
                emb.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")

        else:
            emb = discord.Embed(title=f"Погода в {city_name}",color = discord.Color.orange())
            emb.add_field(name = "Город не найден", value = "by SandwichCommunity")

        await channel.send(embed = emb)
        
async def setup(client):
    await client.add_cog(User(client))

