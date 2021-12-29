import copy
import json
import os
from collections import defaultdict
from io import BytesIO

import discord
from PIL import Image

from utils import get_random_element

script_dir = os.path.dirname(__file__)

weapons_file_path = os.path.join(script_dir, '../resources/json/csgo-weapons.json')
weapons_file = open(weapons_file_path, 'r')
weapons_json = json.load(weapons_file)
weapons_file.close()


class Weapon:
    def __init__(self, name, image):
        self.name = name
        self.image = image


def get_weapons_image(weapons_list):
    images = [
        Image.open(os.path.join(script_dir, '../resources/img/weapons/{}.png'.format(weapon['name'].replace(' ', '_'))))
        for weapon in weapons_list]
    width, height = tuple(s // 4 for s in images[0].size)
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


def generate_weapons_list(weapons_type):
    groups = defaultdict(list)
    for wpn in weapons_json[weapons_type]:
        groups[wpn['group_id']].append(wpn)

    weapons_list = list()
    for wpn_group in groups.values():
        wpn_name = '/'.join([w['name'] for w in wpn_group])
        wpn_image = get_weapons_image(wpn_group)
        weapons_list.append(Weapon(wpn_name, wpn_image))
    return weapons_list


def manage_crw_options(options_str):
    players = list()
    is_unique_weapons = False
    try_help_message = '\nTry `/crw -h` for more information'

    if options_str and not options_str.startswith('-'):
        return None, None, 'Error: Unexpected argument {}{}'.format(options_str.split(' ')[0], try_help_message)

    options = list(filter(None, options_str.split('-')))
    while options:
        args = list(filter(None, options[0].split(' ')))
        option = args[0]
        args.pop(0)
        if option == 'h':
            return None, None, \
                   'CSGO random weapons generator' \
                   '\nUsage: `/crw [-u] [-p] [PLAYER]`' \
                   '\n\nOptions:' \
                   '\n-u                 Generate a unique primary weapon for each player (default is not unique).' \
                   '\n-p string     Generate with a player list, from 1 to 5 player names separated by a space.' \
                   ' By default it will use the nickname or name of the user calling the command.'
        elif option == 'p':
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
            return None, None, 'Error: -{} option is unknown'.format(option, try_help_message)
        options.pop(0)
    if players and len(players) > 5:
        return None, None, 'Error: -p option accepts a maximum of 5 player names'
    return players, is_unique_weapons, None


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


pistols = generate_weapons_list('pistols')
weapons = generate_weapons_list('weapons')
