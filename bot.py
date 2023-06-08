import discord
from discord.ext import commands
import asyncio
import json

intents = discord.Intents.all()
intents.members = True

with open('config.json') as json_file:
    data = json.load(json_file)
    for t in data['config']:
        client = commands.Bot(command_prefix = t['PREFIX'], intents=intents)

client.remove_command("help")

@client.event
async def on_ready():
    print("Bot connected")
    await client.load_extension(f"cogs.user")
    await client.load_extension(f"cogs.admin_com")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        title_error_two = 'Введенная вами команда не существует'
        desc_error_two = 'Используйте **-help**, чтобы просмотреть список доступных команд'
        embed_var_two = discord.Embed(title=title_error_two,
                                      description=desc_error_two,
                                      color=0xFF0000)
        await ctx.reply(embed=embed_var_two)

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    await ctx.send("Загрузка cogs")

@commands.is_owner()
@client.command()
async def unload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")
    await ctx.send("Удаление кога")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")
    await client.load_extension(f"cogs.{extension}")
    await ctx.send("Перезагрузка cogs")

def main():
    client.run(t['TOKEN'])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
