# Bomb Minigame

Name: Bomb Streamlabs Bot  
Version: 1.0.1 
Creator: [marianwulf](https://github.com/marianwulf)  
Description: Multiplayer PVP - use customisable command to pass the bomb to another random target in the viewerlist. If it explodes the bomb holder will lose the defined value and the last holder will get an customisable amount of it. You can adjust all values and responses in the UI.


## Usage

To trigger the bot use !bomb in the chat.

## Installation

1. Please copy the Bomb_StreamlabsSystem.py and UI_Config.json into StreamlabsScriptsFolder/Bomb  
2. Modify the values of the script and save it
3. Disable and enable the script to reinitialise the modified values

## Update

1. Overwrite the Bomb_StreamlabsSystem.py and UI_Config.json to update the script  
(Dont worry, your settings are stored in the settings.json and will not get lost)  
2. Modify new values of the script and save it
3. Disable and enable the script to reinitialise the modified values

## Changelog

### V1.0.1

  - Bugfix: Chatbot sometimes returns empty targetnames as active users, now they will be purged from the viewerlist.

### V1.0.0

  - Enable/Disable using the command when the stream is offline
  - Enable/Disable cooldown
  - Enable/Disable cooldown messages
  - Enable/Disable timeout user when the bomb explodes while holding it
  - Customisable command name
  - Customisable min-max values
  - Costumisable win points percentage
  - Customisable user blacklist
  - Customisable permission for using the command
  - Customisable cooldown timers
  - Customisable timeout amount
  - Customisable response messages
