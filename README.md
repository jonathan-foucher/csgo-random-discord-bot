# Overview
This project is about creating a discord bot for fun *Counter Strike: Global Offensive*.

### CSGO Random Weapon
Generates a random combination of weapon and pistol for the game Counter Strike: Global Offensive.
It's kind of a spin wheel to determine what weapons the player should use during the next match for a challenge/fun purpose.

Some weapons are only available on a side (ct or t) then we decided to regroup them as the game did.

### CSGO Random Map
Get a random CSGO map to know what map you will be playing for the next game.

# Install the project 
Install Python 3 and pip3. Then run the script to install the required libraries :
<br>`sh install-libs.sh`

Create .env file in the ./src directory with your Discord bot token:
<br>`CRWD_BOT_TOKEN=XXXX`

# Start the bot
Create a bot on Discord and invite it on your server with the appropriate permissions.
The bot need to have the permissions to read and write on the channel.
It also works on private message directly with the bot.

Then simply run the main.js file on your server.

# Bot usage

### CSGO Random Weapon
To get a random combination of weapon and pistol, use the `/crw [-u] [-p] [PLAYER]` command. 

The `-h` option displays the information and available options for the command.

The `-p` option allows you to specify from 1 to 5 players name.
<br>If not specified, the default will be the nickname or the name of the player using the command. 
<br>Exemple : `/crw -p Alex John`

For each player to get a unique primary weapon, you have to use the `-u` option.
<br>By default, the players can get the same primary weapon. 
<br>Exemple : `/crw -u -p Alex John`

<img src="resources/img/readme/crw_example.png" alt="Bot answer example for /crw command"/>

### CSGO Random Map
To get a random map, use the `/crm [-b] [-n] [NUMBER]` command.

The `-h` option displays the information and available options for the command.

The `-n` option allows you to generate n map(s). The number must be an integer greater than 0.
<br> It won't send twice the same map. By default, the command will generate a single map.
<br>Exemple : `/crm -n 3`

The `-b` option filters the maps to get only bomb site objective maps.
<br>Exemple : `/crm -b -n 3`

<img src="resources/img/readme/crm_example.png" alt="Bot answer example for /crm command"/>
