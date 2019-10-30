## Synopsis

SirGuy is a simple discord bot with simple music playback features

## Requirements
* System Libraries 
  * FFmpeg
  * opus
* Python Libraries 
  * youtube_dl
  * discord.py
  * PyYAML
  
## Configuration
In order to connect to the Discord API, a bot API key is
required. Create a file called `options.yml` with the following
contents:
```
token: YOUR_DISCORD_BOT_API_TOKEN
```

You can create a new token by going to discordapp.com and
registering a new application.

Once setup, you will need to invite your bot to a discord server.
Then you'll be able to run `python sirguy.py` and enjoy!

## Author

2019 Matthew Emerson

## License

Released under MIT License.