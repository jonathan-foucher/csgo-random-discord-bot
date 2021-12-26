#!/usr/bin/env python3
import json
import os
import random
from collections import defaultdict
from io import BytesIO

import discord
from PIL import Image
from dotenv import load_dotenv

client = discord.Client()
load_dotenv()

script_dir = os.path.dirname(__file__)
weapons_file_path = os.path.join(script_dir, '../resources/json/csgo-weapons.json')
weapons_file = open(weapons_file_path, 'r')
weapons = json.load(weapons_file)
weapons_file.close()


def group_by_group_id(elements):
    groups = defaultdict(list)
    for obj in elements:
        groups[obj['group_id']].append(obj)
    return groups.values()


pistols = list(group_by_group_id(weapons['pistols']))
weapons = list(group_by_group_id(weapons['weapons']))


@client.event
async def on_ready():
    print('Bot is logged as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/crw'):
        random_pistols = get_random_element(pistols)
        random_weapons = get_random_element(weapons)

        images = [get_weapons_image(random_pistols), get_weapons_image(random_weapons)]
        name = message.author.nick if message.author.nick else message.author.name
        response = format_response(name, random_pistols, random_weapons)
        await message.channel.send(response, files=images)


def get_random_element(elements):
    if not elements:
        return
    return random.choice(elements)


def format_response(name, random_pistols, random_weapons):
    return "{} weapons are : {} and {}".format(name, "/".join([p['name'] for p in random_pistols]), "/".join(
        [w['name'] for w in random_weapons]))


def get_weapons_image(weapons_list):
    images = [Image.open(os.path.join(script_dir, '../resources/img/{}.png'.format(weapon['name'].replace(' ', '_'))))
              for weapon in weapons_list]
    width, height = tuple(s//4 for s in images[0].size)
    images = [i.resize((width, height), Image.ANTIALIAS) for i in images]

    total_width = width * len(images)
    combined_im = Image.new('RGBA', (total_width, height))

    x_offset = 0
    for im in images:
        combined_im.paste(im, (x_offset, 0))
        x_offset += width

    with BytesIO() as image_binary:
        combined_im.save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='weapon.png')


client.run(os.getenv('CRWD_BOT_TOKEN'))
