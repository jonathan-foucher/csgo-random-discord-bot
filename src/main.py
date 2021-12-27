#!/usr/bin/env python3
import copy
import os
import random

import discord
from dotenv import load_dotenv

from src.weapon import generate_weapons_list

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

    if message.content.startswith('/crw'):
        pistols_copy = copy.deepcopy(pistols)
        weapons_copy = copy.deepcopy(weapons)

        random_pistol = get_random_element(pistols_copy)
        random_weapon = get_random_element(weapons_copy)

        name = message.author.nick if message.author.nick else message.author.name
        response = "{} weapons are : {} and {}".format(name, random_pistol.name, random_weapon.name)
        images = [random_pistol.image, random_weapon.image]
        await message.channel.send(response, files=images)


def get_random_element(elements):
    if not elements:
        return
    return random.choice(elements)


client.run(os.getenv('CRWD_BOT_TOKEN'))
