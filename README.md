# SparkBot 0.5

## Dependencies
Be sure to pip install discord, discord.py\[voice], youtube_dl, and timeago

ffmpeg is required as well. On linux don't pip install it, you have to use apt-get install ffmpeg

On windows be sure to add both youtube_dl and ffmpeg to the system PATH

## Usage

Create a file named "config.json" following the "config.json.example" file

Create a file in folder "secret" named "private.py" and put a bot token in it

Start "discordBot.py" from src folder

## Update 0.5
- Moved a lot of config information into "config.json", see example file for details
- Added text encryption and decryption capabilities

## Update 0.4
- Added support for Steam API querying
- Moved music commands to their own cog for easier modification
- Fixed "info" command

## Features
- Voice support w/ music
- Discord API querying
- Member whois
- Proxy moderation
- Steam API querying
- Text encryption and decryption, with file support
- And more! see !help for more commands

## Coming soon

- FortniteTracker API querying
