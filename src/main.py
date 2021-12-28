#!/usr/bin/env python3
import copy
import os
import random

import discord
from dotenv import load_dotenv

from weapon import generate_weapons_list

client = discord.Client()
load_dotenv()

pistols = generate_weapons_list('pistols')
weapons = generate_weapons_list('weapons')


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


async def send_random_weapon(channel, players, is_unique_weapons):
    pistols_copy = copy.deepcopy(pistols)
    weapons_copy = copy.deepcopy(weapons)

    for player in players:
        random_pistol = get_random_element(pistols_copy)
        random_weapon = get_random_element(weapons_copy)

        response = '{} weapons are : {} and {}'.format(player, random_pistol.name, random_weapon.name)
        images = [copy.deepcopy(random_pistol.image), copy.deepcopy(random_weapon.image)]
        await channel.send(response, files=images)
        if is_unique_weapons:
            weapons_copy.remove(random_weapon)


def get_random_element(elements):
    if not elements:
        return
    return random.choice(elements)


def manage_crw_options(options_str):
    players = list()
    is_unique_weapons = False

    if options_str and not options_str.startswith('-'):
        return None, None, 'Error: Unexpected argument {}'.format(options_str.split(' ')[0])

    options = list(filter(None, options_str.split('-')))
    while options:
        args = list(filter(None, options[0].split(' ')))
        option = args[0]
        args.pop(0)
        if option == 'p':
            if args:
                players = list(args)
            else:
                return None, None, 'Error: -p option expects from 1 to 5 player names separated by a single space'
        elif option == 'u':
            if args:
                return None, None, 'Error: -u option does not accept arguments'
            else:
                is_unique_weapons = True
        else:
            return None, None, 'Error: -{} option is unknown'.format(option)
        options.pop(0)
    if players and len(players) > 5:
        return None, None, 'Error: -p option accepts a maximum of 5 player names'
    return players, is_unique_weapons, None


client.run(os.getenv('CRWD_BOT_TOKEN'))
