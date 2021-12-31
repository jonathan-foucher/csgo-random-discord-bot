#!/usr/bin/env python3
import os

import discord
from dotenv import load_dotenv

from map import manage_crm_options, send_random_map
from weapon import manage_crw_options, send_random_weapon

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
        players, is_unique_weapons, message_to_send = manage_crw_options(message.content[5:])
        if message_to_send:
            await message.channel.send(message_to_send)
        else:
            if not players:
                players = [message.author.nick if message.author.nick else message.author.name]
            await send_random_weapon(message.channel, players, is_unique_weapons)

    if message.content == '/crm' or message.content.startswith('/crm '):
        number_of_maps, is_bomb_map_only, message_to_send = manage_crm_options(message.content[5:])
        if message_to_send:
            await message.channel.send(message_to_send)
        else:
            await send_random_map(message.channel, number_of_maps, is_bomb_map_only)

    if message.content == '/help' or message.content.startswith('/help '):
        help_message = 'CSGO random bot' \
                       '\n\nCommands:' \
                       '\n/crw    Generate a random combination of primary weapon and pistol.' \
                       '\n/crm    Get random maps.' \
                       '\n\nYou can use `COMMAND -h` to get the help documentation of a command.'
        await message.channel.send(help_message)


client.run(os.getenv('CRWD_BOT_TOKEN'))
