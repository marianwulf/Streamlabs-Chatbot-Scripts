# Hunt Minigame

Name: Hunt Streamlabs Bot  
Version: 1.3.0  
Creator: [marianwulf](https://github.com/marianwulf)  
Description: Multiplayer PVE - use customisable command to fight against 1 of 5 defined bosses. Other players can join the hunt to increase customisable win chances and amounts. You can adjust all values and responses in the UI.


## Usage

To trigger the bot use !hunt in the chat. Other users can join with !joinhunt

## Installation

1. Please copy the Hunt_StreamlabsSystem.py and UI_Config.json into StreamlabsScriptsFolder/Hunt  
2. Modify the values of the script and save it
3. Disable and enable the script to reinitialise the modified values

## Update

1. Overwrite the Hunt_StreamlabsSystem.py and UI_Config.json to update the script  
(Dont worry, your settings are stored in the settings.json and will not get lost)  
2. Modify new values of the script and save it
3. Disable and enable the script to reinitialise the modified values

## Changelog

### V1.3.0
 - Modified code for better usability in the UI (if you are updating from V1.1.X or V1.2.X you need to review your variables in the responses)
 - Added targetname variable to win & lose responses
 - Added currency variable to join fight response

### V1.2.X
 - Customisable minimum attendees to succeed
 - Visual bugfix - max 100% win chance
 - Customisable response messages

### V1.2.0
 - Customisable win chances & win points per attendee
 - Customisable response messages

### V1.1.0
 - Other users can join the hunt
 - Customisable join command name
 - Customisable game timer
 - Customisable response messages

### V1.0.0

 - Enable/Disable using the command when the stream is offline
 - Enable/Disable cooldown / user cooldown / caster cooldown
 - Enable/Disable timeout user on failed attempt
 - Customisable command name
 - Customisable hunt names, win chances, win points, lose points
 - Customisable usage (chat, whisper, both)
 - Customisable permission for using the command
 - Customisable cost for using the command
 - Customisable cooldown / user cooldown timers 
 - Customisable response messages
