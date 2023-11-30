# Nebula - Hypixel
Nebula was designed by `i5` to improve on Lilith, and provide its paid features for free.

## Getting Started:
- Clone this repository or download its code.
- Run `setup.bat` or manually install all the required dependencies(pymchat, pynput, colorama) or Open your command prompt or terminal, navigate to the directory containing the requirements.txt file, and run the following command:
```pip install -r requirements.txt```
- Edit the `config.json` file, enter your Hypixel API Key, and change the settings to your liking.
- Run `start.bat`.

## Setting up AutoRequeue (Optional)
- Go to https://me.lilithmod.xyz/settings/general and enable "Lunar, Unlock blocked Freelook, Autotext, and Minimap" then in game enable Auto Text Hot Key and set 'o' to /lobby classic and 'p' to /rq.

## Features:
- Auto-Dodging
- Free Auto-Requeue
- Free Blacklist-Dodging
- Advanced Antisniper
- Open Source
- Change Requeue Delay
- Clean, Colorful Output

## Limitations:

**Limited Clients**: Only works on Lunar and Default Minecraft clients.

**API Key Requirement**: Will not work without a working hypixel api key, can't piggyback off of lilith for api calls.

**Hypixel API Rate Limiting**: Program adds an extra api call every time you queue. (You will still be well under the limit, and will be imformed if you are close to reaching the 300 requests/5min limit.)

**False Positives**: The nick detection feature is not foolproof and may occasionally produce false positives. This is a Lilith issue, it will be fixed here when nea fixes it.

## Usage:
Start the program, and the startup sequence will be displayed.
Once in a duels game, the program will fetch player statistics.
Players who meet the dodge criteria will be automatically dodged.
If a likely nicked player is detected, they will also be dodged.
The program will provide colorful output for player statistics, dodge decisions, and requeuing notifications.

## Credits:
*Nebula was created by `i5r` based on Lilith v1.0.29 made by nea and their team. The program uses the Hypixel API for fetching player statistics. It also utilizes the pymchat, pynput, and colorama libraries for chat interaction, keyboard control, and colorful output, respectively. Special thanks to the open-source community for their contributions to the development of these libraries. View CREDITS.txt for more.*
