import copy
import glob
import os
import re
from io import BytesIO

import discord
from PIL import Image

from utils import get_random_element

script_dir = os.path.dirname(__file__)
maps_folder = os.path.join(script_dir, '../resources/img/maps/*.png')
maps_paths = glob.glob(maps_folder)


class Map:
    def __init__(self, name, image):
        self.name = name
        self.image = image


def get_maps_image(map_path):
    image = Image.open(map_path)
    width, height = tuple(s // 4 for s in image.size)
    image = image.resize((width, height), Image.ANTIALIAS)

    with BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='map.png')


def generate_maps_list():
    maps_list = list()
    for map_path in maps_paths:
        map_name = re.search('[^\\\\\\/]*\\.(\\w+)$', map_path).group()[:-4]
        map_image = get_maps_image(map_path)
        maps_list.append(Map(map_name, map_image))
    return maps_list


def manage_crm_options(options_str):
    is_bomb_map_only = False
    number_of_maps = 1
    try_help_message = '\nTry `/crm -h` for more information'

    if options_str and not options_str.startswith('-'):
        return None, None, 'Error: Unexpected argument {}{}'.format(options_str.split(' ')[0], try_help_message)

    options = list(filter(None, options_str.split('-')))
    while options:
        args = list(filter(None, options[0].split(' ')))
        option = args[0]
        args.pop(0)
        if option == 'h':
            return None, None, \
                   'CSGO random map generator' \
                   '\nUsage: `/crm [-b] [-n] [NUMBER]`' \
                   '\n\nOptions:' \
                   '\n-b                   Get only bomb site objective maps (default is not only bomb maps).' \
                   '\n-n integer     Define how many maps will be returned (default is 1 map).'
        elif option == 'n':
            if args:
                if len(args) > 1:
                    return None, None, 'Error: -n option expects a single argument'
                if not args[0].isdigit():
                    return None, None, 'Error: -n option expects an integer'
                n = int(args[0])
                if n == 0:
                    return None, None, 'Error: -n option expects an integer greater than 0'
                number_of_maps = n
            else:
                return None, None, 'Error: -n option expects an integer in argument'
        elif option == 'b':
            if args:
                return None, None, 'Error: -b option does not accept arguments'
            else:
                is_bomb_map_only = True
        else:
            return None, None, 'Error: -{} option is unknown'.format(option, try_help_message)
        options.pop(0)

        if number_of_maps > len(maps):
            return None, None, 'Error: You are asking for {} maps but there is only {} available'.format(
                number_of_maps, len(maps))
        if is_bomb_map_only and number_of_maps > len([m for m in maps if m.name.startswith('de_')]):
            return None, None, 'Error: You are asking for {} maps but there is only {} available with -b option'.format(
                number_of_maps, len([m for m in maps if m.name.startswith('de_')]))

    return number_of_maps, is_bomb_map_only, None


async def send_random_map(channel, number_of_maps, is_bomb_map_only):
    if is_bomb_map_only:
        maps_copy = copy.deepcopy([m for m in maps if m.name.startswith('de_')])
    else:
        maps_copy = copy.deepcopy(maps)
    for i in range(number_of_maps):
        random_map = get_random_element(maps_copy)
        response = 'You will be playing on {}'.format(random_map.name)
        await channel.send(response, file=copy.deepcopy(random_map.image))
        maps_copy.remove(random_map)


maps = generate_maps_list()
