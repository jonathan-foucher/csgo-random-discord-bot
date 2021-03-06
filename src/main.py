#!/usr/bin/env python3
import os

import discord
from dotenv import load_dotenv

from map import send_random_map
from weapon import send_random_weapon

client = discord.Client()
load_dotenv()


@client.event
async def on_ready():
    print('Bot is logged as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '/crw' or message.content.startswith('/crw '):
        await send_random_weapon(message)

    if message.content == '/crm' or message.content.startswith('/crm '):
        await send_random_map(message)

    if message.content == '/help' or message.content.startswith('/help '):
        help_message = 'CSGO random bot' \
                       '\n\nCommands:' \
                       '\n/crw    Generate a random combination of primary weapon and pistol.' \
                       '\n/crm    Get random maps.' \
                       '\n\nYou can use `COMMAND -h` to get the help documentation of a command.'
        await message.channel.send(help_message)


client.run(os.getenv('CRWD_BOT_TOKEN'))
