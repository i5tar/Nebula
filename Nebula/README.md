Nebula - Hypixel

Nebula was designed by `i5` to improve on lilith, and provide its paid features for free.

SETUP:
- Find config.json and enter your Hypixel API key and change the settings to your liking.
- Find Nebula.exe and run it to get started!

SETUP FOR AUTO RQ:
- Go to https://me.lilithmod.xyz/settings/general and enable "Lunar, Unlock blocked Freelook, Autotext, and Minimap" then in game enable Auto Text Hot Key and set 'o' to /lobby classic and 'p' to /rq.

Features:

- Auto-Dodging
- Free Auto-Requeue
- Free Blacklist-Dodging
- Advanced Antisniper
- Open Source
- Change Requeue Delay
- Clean, Colorful Output

Limitations:

API Key Requirement: Will not work without a working hypixel api key, can't piggyback off of lilith for api calls.

Hypixel API Rate Limiting: Program adds an extra api call every time you queue. (You will still be well under the limit, and will be imformed if you are close to reaching the 300 requests/5min limit.)

False Positives: The nick detection feature is not foolproof and may occasionally produce false positives. Users should use their discretion when dodging players based on nick detection. This is a Lilith issue, it will be fixed here when nea fixes it.

Usage:
Start the program, and the startup sequence will be displayed.
Once in a duels game, the program will fetch chat messages and player statistics.
Players who meet the dodge criteria will be automatically dodged.
If a likely nicked player is detected, they will also be dodged.
The program will provide colorful output for player statistics, dodge decisions, and requeuing notifications.

Caution:
Use this program responsibly and in compliance with Hypixel's rules and terms of service.
Avoid spamming the Hypixel API to prevent rate limiting and possible penalties.
Disclaimer:
This program is not officially affiliated with Hypixel or Mojang. Use at your own risk. The developers are not responsible for any consequences arising from the use of this program.

Credits:
Better Lilith was created by `i5r` based on lilith v1.0.29 made by nea and their team. The program uses the Hypixel API for fetching player statistics. It also utilizes the pymchat, pynput, and colorama libraries for chat interaction, keyboard control, and colorful output, respectively. Special thanks to the open-source community for their contributions to the development of these libraries. View CREDITS.txt for more.