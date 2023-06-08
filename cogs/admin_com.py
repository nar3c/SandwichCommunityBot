import discord
from discord import permissions
from discord import colour
from discord.ext import commands
from discord.utils import get
import asyncio
from bot import client

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
#   @commands.has_any_role()
    async def mute(self, ctx, member: discord.Member, time: int, *, args):
        try:
            await ctx.reply(embed = discord.Embed(color = discord.Color.from_rgb(155, 267, 246), description = "-mute [ник] [время] [причина]"))

        except discord.ext.commands.errors.MissingRequiredArgument:
            role = discord.utils.get(ctx.message.guild.roles, name='МУТ')
            if role == None:
                perms = discord.Permissions(2048)
                await ctx.author.guild.create_role(name="МУТ", permissions=perms)

            print(f'{ctx.author} muted {member}')
            await member.add_roles(discord.utils.get(ctx.message.guild.roles, name='МУТ'))
            embed = discord.Embed(
                title = 'НАКАЗАНИЕ',
                description = f'Здравствуй, {member.mention}!\n \nТы нарушил правило:\n{args}\nДлительность мута: {time} минут.\n \nНадеемся на дальнейшее неповторение\nэтой ситуации и на Ваше исправление.',
                colour = discord.colour.Colour.orange()
            )

            embed.set_author(name = "Sandwich Community", icon_url = 'https://cdn.discordapp.com/attachments/968956363558494218/968979654042071120/sandwich_art.jpg')
            embed.set_footer(text = "С уважением. Администрация Сообщества.")
            await ctx.reply(embed = embed)

            await asyncio.sleep(time * 60)
            await member.remove_roles(discord.utils.get(ctx.message.guild.roles, name = 'МУТ'))

    @commands.command()
#   @commands.has_any_role()
    async def ban(self, ctx, member: discord.Member, *, reason):
        await ctx.guild.ban(member)
        print(f'{ctx.author} banned {member}')
        await ctx.reply(embed = discord.Embed(color = discord.Color.from_rgb(166, 245, 255), description = f"Пользователь {member.mention} был забанен по причине {reason}"))

    @commands.command()
#   @commands.has_any_role()
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.reply(embed = discord.Embed(color = discord.Color.from_rgb(155, 267, 246), description = f"Пользователь {member} был разбанен"))

    @commands.command()
#   @commands.has_any_role()
    async def unmute(self, ctx, member: discord.Member):
        await member.remove_roles(discord.utils.get(ctx.message.guild.roles, name = 'МУТ'))
        await ctx.reply(":white_check_mark:")

    @commands.command()
#   @commands.has_any_role()
    async def send(self, ctx, name, *, text):
        channel = discord.utils.get(ctx.author.guild.channels, name=name)
        await channel.send(f"{text}")

    @commands.command()
#   @commands.has_any_role()
    async def embed(self, ctx, name, *, text):
        channel = discord.utils.get(ctx.author.guild.channels, name=name)
        embed = discord.Embed(color = discord.Color.orange(), description = f"{text}")
        embed.set_author(name = "Sandwich Community", icon_url = "https://cdn.discordapp.com/attachments/968956363558494218/968979654042071120/sandwich_art.jpg")
        await channel.send(embed = embed)

    @commands.command()
#   @commands.has_any_role()
    async def clear(self, ctx, amount: int):
        embed = discord.Embed(color = discord.Color.orange(), description = "Очистка♻️")
        await asyncio.sleep(2)
        print(f'{ctx.author} cleared chat')
        await ctx.channel.purge(limit = amount + 1)

async def setup(client):
    await client.add_cog(Admin(client))
