# Better Lilith - Hypixel

Better Lilith was designed by `i5r` in Python to improve on lilith, and provide its paid features for free.

## Features:

- Auto-Dodging
- Free Auto-Requeue
- Free Blacklist-Dodging
- Advanced Antisniper
- Open Source
- Change Requeue Delay
- Clean, Colorful Output

## Getting Started:
1. Ensure Python and the required libraries (pymchat, pynput, and colorama) are installed.
    - Open your command prompt or terminal, navigate to the directory containing the requirements.txt file, and run the following command:
    ```pip install -r requirements.txt```
2. Find `config.json`, enter your Hypixel API key and adjust the settings to your liking.
3. Run `start.bat`.

## Setting up autododge:
1. Go to https://me.lilithmod.xyz/settings/general and enable "Lunar, Unlock blocked Freelook, Autotext, and Minimap" then in game enable Auto Text Hot Key and set 'o' to `/lobby classic` and 'p' to `/rq`.

## Limitations:

**Limited Clients**: Will only work on Lunar and Default Minecraft client.

**API Key Requirement**: Will not work without a working hypixel api key, can't piggyback off of lilith for api calls.

**Hypixel API Rate Limiting**: Program adds an extra api call per time you queue. (You will still be well under the limit, and will be imformed if you are close to reaching the 300 requests/5min limit.)

**Dependency on Third-Party Libraries**: The program relies on third-party libraries, such as pymchat, pynput, and colorama, for chat functionality, keyboard control, and color output, respectively.

**False Positives**: The nick detection feature is not foolproof and may occasionally produce false positives. This is a lilith issue, so I can't fix it.

## Usage:
Start the program, and the startup sequence will be displayed.
Once in a duels game, the program will fetch player statistics.
Players who meet the dodge criteria will be automatically dodged.
If a likely nicked player is detected, they will also be dodged.
The program will provide colorful output for player statistics, dodge decisions, and requeuing notifications.

## Disclaimer:
This program is not officially affiliated with Hypixel or Mojang. Use at your own risk. The developers are not responsible for any consequences arising from the use of this program.

## Credits:
*Better Lilith was created by `i5r` based on lilith v1.0.29 made by nea and thier team. The program uses the Hypixel API for fetching player statistics. It also utilizes the pymchat, pynput, and colorama libraries for chat interaction, keyboard control, and colorful output, respectively. Special thanks to the open-source community for their contributions to the development of these libraries.*