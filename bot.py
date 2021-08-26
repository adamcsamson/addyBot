# bot.py
import os
from pprint import pprint
import requests
from blizzardapi import BlizzardApi
import discord
from dotenv import load_dotenv
import wowItemLookup

load_dotenv()
TOKEN = '#'
GUILD = '#' #SERVER
blizz_client = '#'
blizz_secret = '#'
client = discord.Client()
api_client = BlizzardApi('#', '#')


@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Kings honor, {member.name}. Welcome to <On Craft>')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if '!item' in message.content.lower():
        normalItemName = ""
        splitMessage = message.content.split()
        searchTerm = wowItemLookup.parseKeyword(splitMessage)
        for seperated in splitMessage[1:]:
            normalItemName += (seperated + " ")
        print("searching " + normalItemName + " with search_term: " + searchTerm)
        response = wowItemLookup.displayItemStats(searchTerm, normalItemName)
        await message.channel.send(response)


client.run(TOKEN)