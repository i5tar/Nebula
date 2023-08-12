import json
import requests
import time
import math
import os
from pymchat.chat import Chat
from pynput.keyboard import Key, Controller
from colorama import init, Fore, Style
from pathlib import Path
import ctypes
import sys

ctypes.windll.kernel32.SetConsoleTitleW("Nebula")

keyboard = Controller()
init()  # Initialize colorama

# Code Begins

chat = Chat()

# Dictionary to store the already printed IGNs with timestamp
printed_igns = {}

# Startup sequence
print("Nebula Stable Release 1" + Style.RESET_ALL)
print("================================")
time.sleep(0.5)
print(Fore.RED + "Version » " + Style.RESET_ALL + "v1.1.3")
time.sleep(0.5)

# Function to fetch the configuration from the config.json file
def fetch_config():
    # Get the absolute path of the script
    script_path = os.path.abspath(sys.argv[0])

    # Get the directory containing the script
    script_dir = os.path.dirname(script_path)
    config_file_path = os.path.join(script_dir, "config.json")
    
    if os.path.exists(config_file_path):
        print(Fore.YELLOW + "Config » " + Style.RESET_ALL + "Fetching [...]", end="", flush=True)
        time.sleep(1)  # Simulate fetching delay, remove this line in production
        with open(config_file_path) as f:
            config = json.load(f)
        
        api_key = config.get("api_key")
        if api_key == "HYPIXEL_API_KEY_HERE":
            print("\r" + Fore.RED + "Error » " + Style.RESET_ALL + "Please enter your Hypixel API key into config.json", flush=True)
        else:
            print("\r" + Fore.YELLOW + "Config » " + Style.RESET_ALL + "Fetched!      ", flush=True)
            time.sleep(0.01)
            print(Fore.GREEN + "Ready » " + Style.RESET_ALL + "Queue once in-game")
        return config
    else:
        print(Fore.RED + "Error: config.json not found. Please make sure the configuration file exists." + Style.RESET_ALL)
        sys.exit(1)

# Fetch the configuration
config = fetch_config()

# Access the configuration settings
api_key = config["api_key"]
requeue_delay = config["requeue_delay"]
gamemode = config["gamemode"]
ShowGamemode = config["ShowGamemode"]
AntiSniper = config["AntiSniper"]
AutoDodge = config["AutoDodge"]
DodgeNicks = config["DodgeNicks"]

max_wins = config["max_wins"]
min_wins = config["min_wins"]
max_losses = config["max_losses"]
min_losses = config["min_losses"]
max_wlr = config["max_wlr"]
min_wlr = config["min_wlr"]
max_current_ws = config["max_current_ws"]
min_current_ws = config["min_current_ws"]
max_best_ws = config["max_best_ws"]
min_best_ws = config["min_best_ws"]

min_network_level = config["min_network_level"]
max_skywars_star = config["max_skywars_star"]
max_skywars_kdr = config["max_skywars_kdr"]
max_bedwars_star = config["max_bedwars_star"]
max_bedwars_fkdr = config["max_bedwars_fkdr"]
max_bedwars_bblr = config["max_bedwars_bblr"]
max_bedwars_kdr = config["max_bedwars_kdr"]
max_bedwars_finals_per_star = config["max_bedwars_finals_per_star"]
max_sumo_wlr = config["max_sumo_wlr"]
max_sumo_bws = config["max_sumo_bws"]
max_uhc_duels_wlr = config["max_uhc_duels_wlr"]
max_uhc_kdr = config["max_uhc_kdr"]
max_overall_wlr = config["max_overall_wlr"]
max_overall_wins = config["max_overall_wins"]
min_overall_wins = config["min_overall_wins"]
min_overall_losses = config["min_overall_losses"]
max_overall_bws = config["max_overall_bws"]
max_overall_cws = config["max_overall_cws"]
max_melee_accuracy = config["max_melee_accuracy"]
max_combo_maccuracy = config["max_combo_maccuracy"]

dodge_igns = config["dodge_igns"]

# A flag to keep track if a player is already queued
already_queued = False
rounding_precision = 3
capgamemode = gamemode.capitalize()

def fetch_player_uuid(player_name):
    try:
        url = f"https://api.mojang.com/users/profiles/minecraft/{player_name}"
        response = requests.get(url)
        data = json.loads(response.text)

        if 'id' in data:
            player_uuid = data['id']
            return player_uuid

    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
        print("An error occurred while fetching the player's UUID." + Style.RESET_ALL)

    return None

def fetch_player_stats(player_uuid):
    try:
        url = f"https://api.hypixel.net/player?key={api_key}&uuid={player_uuid}"
        response = requests.get(url)
        data = json.loads(response.text)

        if 'player' in data:
            player_stats = data['player']['stats']['Duels']
            duels_wins = player_stats.get(f'{gamemode}_duel_wins', 0)
            duels_losses = player_stats.get(f'{gamemode}_duel_losses', 0)
            duels_winstreak = player_stats.get(f'current_{gamemode}_winstreak', 0)
            best_winstreak = player_stats.get(f'best_{gamemode}_winstreak', 0)

            if antisniper:
                overall_wins = player_stats.get('wins', 0)
                overall_losses = player_stats.get('losses', 0)
                overall_duels_winstreak = player_stats.get('current_winstreak', 0)
                overall_best_winstreak = player_stats.get('best_overall_winstreak', 0)

                try:
                    player_stats = data['player']['stats']['Bedwars']
                    bedwars_wins = player_stats.get('wins_bedwars', 0)
                    bedwars_losses = player_stats.get('losses_bedwars', 0)
                    bedwars_winstreak = player_stats.get('winstreak', 0)
                    bedwars_final_kills = player_stats.get('final_kills_bedwars', 0)
                    bedwars_final_deaths = player_stats.get('final_deaths_bedwars', 0)

                except KeyError:
                    print(Fore.YELLOW + f"Nebula > Couldn't find bedwars stats" + Style.RESET_ALL)
                    bedwars_wins = bedwars_losses = bedwars_winstreak = bedwars_final_kills = bedwars_final_deaths = None

                return (duels_wins, duels_losses, duels_winstreak, best_winstreak, overall_wins, overall_losses,
                        overall_duels_winstreak, overall_best_winstreak, bedwars_wins, bedwars_losses, 
                        bedwars_winstreak, bedwars_final_kills, bedwars_final_deaths)

            else:
                return (duels_wins, duels_losses, duels_winstreak, best_winstreak, None, None, None, None, None, None, None, None, None, None)

    except Exception as e:
        print(f"Error: {e}")


def calculate_ratio(wins, losses):
    if losses == 0:
        return wins
    else:
        return wins / losses

# colors lol
class c:
    Default      = "\033[39m"
    Black        = "\033[30m"
    Red          = "\033[31m"
    Green        = "\033[32m"
    Yellow       = "\033[33m"
    Blue         = "\033[34m"
    Magenta      = "\033[35m"
    Cyan         = "\033[36m"
    LightGray    = "\033[37m"
    Pink         = "\033[38m"
    DarkGray     = "\033[90m"
    LightRed     = "\033[91m"
    LightGreen   = "\033[92m"
    LightYellow  = "\033[93m"
    LightBlue    = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan    = "\033[96m"
    White        = "\033[97m"

    bgDefault      = "\033[49m"
    bgBlack        = "\033[40m"
    bgRed          = "\033[41m"
    bgGreen        = "\033[42m"
    bgYellow       = "\033[43m"
    bgBlue         = "\033[44m"
    bgMagenta      = "\033[45m"
    bgCyan         = "\033[46m"
    bgLightGray    = "\033[47m"
    bgPink         = "\033[48m"
    bgDarkGray     = "\033[100m"
    bgLightRed     = "\033[101m"
    bgLightGreen   = "\033[102m"
    bgLightYellow  = "\033[103m"
    bgLightBlue    = "\033[104m"
    bgLightMagenta = "\033[105m"
    bgLightCyan    = "\033[106m"
    bgWhite        = "\033[107m"

    stItalics            = "\033[206m"
    stUnderline          = "\033[206m"
    stDoubleUnderline    = "\033[206m"
    stBold               = "\033[1m"
    allDefault           = "\033[0m"

class bcolors:
    White        = "\033[97m"
    BackgroundDefault      = "\033[49m"


def getInfo(call):
    r = requests.get(call)
    return r.json()

# Declare the global variable stat_bedwars_star and initialize it to None
stat_bedwars_star = None

def antisniper():
    global stat_bedwars_star
    print(f"{bcolors.BackgroundDefault}{bcolors.White}┏━━━━━━━━━━━━━━━━ AntiSniper")

    try:
        resp = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}")
        uuid = resp.json()["id"]

    except KeyError:
        print("\n-MOJANG API ERROR-\n")

    

    url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
    
    data = getInfo(url)

# BEDWARS
    try:
        stat_bedwars_star = data["player"]["achievements"]["bedwars_level"]
    except KeyError:
        stat_bedwars_star = 0
    try:
        stat_bedwars_final_kills = data["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
    except KeyError:
        stat_bedwars_final_kills = 0
    try:
        stat_bedwars_final_deaths = data["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
    except KeyError:
        stat_bedwars_final_deaths = 0
    try:
        stat_bedwars_beds_broken = data["player"]["stats"]["Bedwars"]["beds_broken_bedwars"]
    except KeyError:
        stat_bedwars_beds_broken = 0
    try:
        stat_bedwars_beds_lost = data["player"]["stats"]["Bedwars"]["beds_lost_bedwars"]
    except KeyError:
        stat_bedwars_beds_lost = 0
    
    stat_bblr = round((stat_bedwars_beds_broken/max(stat_bedwars_beds_lost,1)),rounding_precision)


    
    # SKYWARS
    try:
        stat_level_formatted = data["player"]["stats"]["SkyWars"]["levelFormatted"]
    except KeyError:
        stat_level_formatted = "xx0x"
    try:
        stat_skywars_kills = data["player"]["stats"]["SkyWars"]["kills"]
    except KeyError:
        stat_skywars_kills = 0
    try:
        stat_skywars_deaths = data["player"]["stats"]["SkyWars"]["deaths"]
    except KeyError:
        stat_skywars_deaths = 0


    stat_fkdr = round((stat_bedwars_final_kills/max(stat_bedwars_final_deaths,1)), rounding_precision)
    stat_skywars_kdr = round((stat_skywars_kills/max(stat_skywars_deaths,1)), rounding_precision)

    # SUMO
    try:
        stat_sumo_duel_wins = data["player"]["stats"]["Duels"]["sumo_duel_wins"]
    except KeyError:
        stat_sumo_duel_wins = 0
    try:
        stat_sumo_duel_losses = data["player"]["stats"]["Duels"]["sumo_duel_losses"]
    except KeyError:
        stat_sumo_duel_losses = 0
        
    sumowlr = round((stat_sumo_duel_wins/max(stat_sumo_duel_losses, 1)), rounding_precision)

    try:
        stat_sumo_bws = data["player"]["stats"]["Duels"]["best_sumo_winstreak"]
    except KeyError:
        stat_sumo_bws = 0


    # UHC DUELS
    try:
        stat_uhc_duel_wins = data["player"]["stats"]["Duels"]["uhc_duel_wins"]
    except KeyError:
        stat_uhc_duel_wins = 0

    try:
        stat_uhc_duel_losses = data["player"]["stats"]["Duels"]["uhc_duel_losses"]
    except KeyError:
        stat_uhc_duel_losses = 0

    uhcwlr = round((stat_uhc_duel_wins/max(stat_uhc_duel_losses, 1)), rounding_precision)
    
    # REAL UHC
    try:
        stat_UHC_kills = data["player"]["stats"]["UHC"]["kills_solo"] + data["player"]["stats"]["UHC"]["kills"]
    except KeyError:
        stat_UHC_kills = 0

    try:
        stat_UHC_deaths = data["player"]["stats"]["UHC"]["deaths_solo"] + data["player"]["stats"]["UHC"]["deaths"]
    except KeyError:
        stat_UHC_deaths = 0

    uhckdr = round((stat_UHC_kills/max(stat_UHC_deaths, 1)), rounding_precision)

    # All Duels
    try:
        stat_duels_wins = data["player"]["stats"]["Duels"]["wins"]
    except KeyError:
        stat_duels_wins = 0

    try:
        stat_duels_losses = data["player"]["stats"]["Duels"]["losses"]
    except KeyError:
        stat_duels_losses = 0

    try:
        stat_duels_bws = data["player"]["stats"]["Duels"]["best_overall_winstreak"]
    except KeyError:
        stat_duels_bws = 0

    try:
        stat_duels_cws = data["player"]["stats"]["Duels"]["current_winstreak"]
    except KeyError:
        stat_duels_cws = 0

    # Bedwars
    try:
        stat_bw_kills = data["player"]["stats"]["Bedwars"]["kills_bedwars"]
    except KeyError:
        stat_bw_kills = 0

    try:
        stat_bw_deaths = data["player"]["stats"]["Bedwars"]["deaths_bedwars"]
    except KeyError:
        stat_bw_deaths = 0
    
    # Melee
    try:
        stat_duels_melee_hits = data["player"]["stats"]["Duels"]["melee_hits"]
    except KeyError:
        stat_duels_melee_hits = 0

    try:
        stat_duels_melee_swings = data["player"]["stats"]["Duels"]["melee_swings"]
    except KeyError:
        stat_duels_melee_swings = 0

    try:
        stat_duels_combo_melee_hits = data["player"]["stats"]["Duels"]["combo_duel_melee_hits"]
    except KeyError:
        stat_duels_combo_melee_hits = 0

    try:
        stat_duels_combo_melee_swings = data["player"]["stats"]["Duels"]["combo_duel_melee_swings"]
    except KeyError:
        stat_duels_combo_melee_swings = 0

    try:
        hypixelxp = data["player"]["networkExp"]
    except KeyError:
        hypixelxp = 0

    nwl = round(((math.sqrt((2 * hypixelxp) + 30625) / 50) - 2.5), rounding_precision)
    

    nocombomeleehits = stat_duels_melee_hits-stat_duels_combo_melee_hits
    nocombomeleeswings = stat_duels_melee_swings-stat_duels_combo_melee_swings

    stat_melee_accuracy = round((nocombomeleehits/max(nocombomeleeswings,1)*100), rounding_precision)


    stat_bw_kdr = round(stat_bw_kills/max(stat_bw_deaths,1), rounding_precision)
    stat_bw_fksperstar = round(stat_bedwars_final_kills/max(stat_bedwars_star,1), rounding_precision)

    tDanger = f'{c.White}{c.bgRed}┃DANGER{c.bgDefault}'
    tRisky = f'{c.Yellow}┃Risky{c.White}'
    tSafe = f'{c.White}┃Safe'


    wlr = round((stat_duels_wins/max(stat_duels_losses, 1)), rounding_precision)

    swstar = stat_level_formatted[2:-1]+" ☆"
    intswstar = int(stat_level_formatted[2:-1])

    bwstar = str(stat_bedwars_star)+" ☆"

    stat_combo_melee_accuracy = round((stat_duels_combo_melee_hits/max(stat_duels_combo_melee_swings,1)*100), rounding_precision)
    print(f"{c.bgDefault}{c.DarkGray}┃ IGN:", ign)
    print(f"{c.bgDefault}{c.DarkGray}┃ UUID:", uuid)
    print(f"{c.bgDefault}{c.White}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    if 15 < nwl < 100:
        print(f"{tSafe}    ||   NWL: {nwl}") 
    elif (100 < nwl < 200) or (5 < nwl < 15):
        print(f"{tRisky}   ||   NWL: {c.Yellow}{nwl}")
    elif nwl < 5:
        print(f"{tDanger}  ||   NWL: {c.Red}{nwl}")
    else:
        print(f"{tDanger}  ||   NWL: {c.Red}{nwl}")


    if 0 < intswstar < 10:
        print(f"{tSafe}    ||   SW star: {swstar}")
    elif intswstar < 15 or intswstar == 0:
        print(f"{tRisky}   ||   SW star: {c.Yellow}{swstar}")
    elif intswstar > 15:
        print(f"{tDanger}  ||   SW star: {c.Red}{swstar}")

    # time.sleep(0.005)
    
    if stat_skywars_kdr < 1:
        print(f"{tSafe}    ||   SW kdr: {stat_skywars_kdr}")
    elif stat_skywars_kdr > 1 and stat_skywars_kdr < 2:
        print(f"{tRisky}   ||   SW kdr: {c.Yellow}{stat_skywars_kdr}")
    elif stat_skywars_kdr > 2:
        print(f"{tDanger}  ||   SW kdr: {c.Red}{stat_skywars_kdr}")
    
    # time.sleep(0.005)
    
    if stat_bedwars_star < 200 and stat_bedwars_star != 0:
        print(f"{tSafe}    ||   BW star: {stat_bedwars_star} ☆")
    elif stat_bedwars_star > 200 and stat_bedwars_star < 350:
        print(f"{tRisky}   ||   BW star: {c.Yellow}{stat_bedwars_star} ☆")
    elif stat_bedwars_star > 350 or stat_bedwars_star == 0:
        print(f"{tDanger}  ||   BW star: {c.Red}{stat_bedwars_star} ☆")

    # time.sleep(0.005)
    
    if stat_fkdr < 2 and stat_fkdr != 0:
        print(f"{tSafe}    ||   FKDR: {stat_fkdr}")
    elif stat_fkdr > 2 and stat_fkdr < 3.5:
        print(f"{tRisky}   ||   FKDR: {c.Yellow}{stat_fkdr}")
    elif stat_fkdr > 3.5:
        print(f"{tDanger}  ||   FKDR: {c.Red}{stat_fkdr}")
    else:
        print(f"{tRisky}   ||   FKDR: {c.Yellow}{stat_fkdr}")


    # time.sleep(0.005)

    if stat_bblr < 1.4 and stat_bblr != 0:
        print(f"{tSafe}    ||   BBLR: {stat_bblr}")
    elif stat_bblr > 1.4 and stat_bblr < 2.8:
        print(f"{tRisky}   ||   BBLR: {c.Yellow}{stat_bblr}")
    elif stat_bblr > 2.8:
        print(f"{tDanger}  ||   BBLR: {c.Red}{stat_bblr}")
    else:
        print(f"{tRisky}   ||   BBLR: {c.Yellow}{stat_bblr}")
    

    # time.sleep(0.005)
    
    if stat_bw_kdr < 1.2:
        print(f"{tSafe}    ||   BW kdr: {stat_bw_kdr}")
    elif stat_bw_kdr > 1.2 and stat_bw_kdr < 2.4:
        print(f"{tRisky}   ||   BW kdr: {c.Yellow}{stat_bw_kdr}")
    elif stat_bw_kdr > 2.4:
        print(f"{tDanger}  ||   BW kdr: {c.Red}{stat_bw_kdr}")

    # time.sleep(0.005)
    
    if stat_bw_fksperstar < 25:
        print(f"{tSafe}    ||   BW fks/star: {stat_bw_fksperstar}")
    elif stat_bw_fksperstar > 25 and stat_bw_fksperstar < 50:
        print(f"{tRisky}   ||   BW fks/star: {c.Yellow}{stat_bw_fksperstar}")
    elif stat_bw_fksperstar > 50:
        print(f"{tDanger}  ||   BW fks/star: {c.Red}{stat_bw_fksperstar}")

    # time.sleep(0.005)
    
    if sumowlr < 1.5:
        print(f"{tSafe}    ||   Sumo wlr: {sumowlr}")
    elif sumowlr > 1.5 and sumowlr < 2.25:
        print(f"{tRisky}   ||   Sumo wlr: {c.Yellow}{sumowlr}")
    elif sumowlr > 2.25:
        print(f"{tDanger}  ||   Sumo wlr: {c.Red}{sumowlr}")

    # time.sleep(0.005)
    
    if stat_sumo_bws < 10 and stat_sumo_bws != 0:
        print(f"{tSafe}    ||   Sumo bws: {stat_sumo_bws}")
    elif stat_sumo_bws > 10 and stat_sumo_bws < 25:
        print(f"{tRisky}   ||   Sumo bws: {c.Yellow}{stat_sumo_bws}")
    elif stat_sumo_bws > 25 or (stat_sumo_bws == 0 and stat_sumo_duel_wins > 0):
        print(f"{tDanger}  ||   Sumo bws: {c.Red}{stat_sumo_bws}")
    else:
        print(f"{tRisky}   ||   Sumo bws: {c.Yellow}{stat_sumo_bws}")

    # time.sleep(0.005)
    
    if uhcwlr < 1:
        print(f"{tSafe}    ||   UHCD wlr: {uhcwlr}")
    elif uhcwlr > 1 and uhcwlr < 2.5:
        print(f"{tRisky}   ||   UHCD wlr: {c.Yellow}{uhcwlr}")
    elif uhcwlr > 2.5:
        print(f"{tDanger}  ||   UHCD wlr: {c.Red}{uhcwlr}")

    # time.sleep(0.005)
    
    if uhckdr < 0.5:
        print(f"{tSafe}    ||   UHC kdr: {uhckdr}")
    elif uhckdr > 0.5 and uhckdr < 1.5:
        print(f"{tRisky}   ||   UHC kdr: {c.Yellow}{uhckdr}")
    elif uhckdr > 1.5:
        print(f"{tDanger}  ||   UHC kdr: {c.Red}{uhckdr}")

    # time.sleep(0.005)
    
    if wlr < 1.5 or (wlr == 0 and stat_duels_losses > 0):
        print(f"{tSafe}    ||   Wlr: {wlr}")
    elif wlr > 1.5 and wlr < 2.5:
        print(f"{tRisky}   ||   Wlr: {c.Yellow}{wlr}")
    elif wlr > 2.5 or (wlr == 0 and stat_duels_losses == 0):
        print(f"{tDanger}  ||   Wlr: {c.Red}{wlr}")

    # time.sleep(0.005)
    
    if stat_duels_wins > 10 and stat_duels_wins < 10000:
        print(f"{tSafe}    ||   Wins: {stat_duels_wins}")
    elif (stat_duels_wins > 3 and stat_duels_wins < 10) or (stat_duels_wins > 10000 and stat_duels_wins < 20000):
        print(f"{tRisky}   ||   Wins: {c.Yellow}{stat_duels_wins}")
    elif (stat_duels_wins < 3 and (stat_duels_losses < 4 * stat_duels_wins)) or (stat_duels_wins > 20000):
        print(f"{tDanger}  ||   Wins: {c.Red}{stat_duels_wins}")
    else:
        print(f"{tSafe}    ||   Wins: {stat_duels_wins}")

    # time.sleep(0.005)

    if stat_duels_losses > 10:
        print(f"{tSafe}    ||   Losses: {stat_duels_losses}")
    elif stat_duels_losses > 3 and stat_duels_losses < 10:
        print(f"{tRisky}   ||   Losses: {c.Yellow}{stat_duels_losses}")
    elif stat_duels_losses < 3:
        print(f"{tDanger}  ||   Losses: {c.Red}{stat_duels_losses}")
    else:
        print(f"{tSafe}    ||   Losses: {stat_duels_losses}")

    # time.sleep(0.01)
    
    if stat_duels_bws < 25 and stat_duels_bws != 0:
        print(f"{tSafe}    ||   Bws: {stat_duels_bws}")
    elif stat_duels_bws > 25 and stat_duels_bws < 50:
        print(f"{tRisky}   ||   Bws: {c.Yellow}{stat_duels_bws}")
    elif stat_duels_bws > 50 or stat_duels_bws == 0:
        print(f"{tDanger}  ||   Bws: {c.Red}{stat_duels_bws}")

    # time.sleep(0.01)
    
    if stat_duels_cws < 5:
        print(f"{tSafe}    ||   Cws: {stat_duels_cws}")
    elif stat_duels_cws > 5 and stat_duels_cws < 15:
        print(f"{tRisky}   ||   Cws: {c.Yellow}{stat_duels_cws}")
    elif stat_duels_cws > 15:
        print(f"{tDanger}  ||   Cws: {c.Red}{stat_duels_cws}")

    # time.sleep(0.01)
    
    if stat_melee_accuracy < 50 and stat_melee_accuracy != 0:
        print(f"{tSafe}    ||   mAccuracy: {stat_melee_accuracy} %")
    elif stat_melee_accuracy > 50 and stat_melee_accuracy < 70:
        print(f"{tRisky}   ||   mAccuracy: {c.Yellow}{stat_melee_accuracy} %")
    elif stat_melee_accuracy > 70 or stat_melee_accuracy == 0:
        print(f"{tDanger}  ||   mAccuracy: {c.Red}{stat_melee_accuracy} %")

    # time.sleep(0.01)
    
    if stat_combo_melee_accuracy < 75:
        print(f"{tSafe}    ||   Combo mAcc: {stat_combo_melee_accuracy} %")
    elif stat_combo_melee_accuracy > 75 and stat_combo_melee_accuracy < 100:
        print(f"{tRisky}   ||   Combo mAcc: {c.Yellow}{stat_combo_melee_accuracy} %{c.Default}")
    elif stat_combo_melee_accuracy > 100:
        print(f"{tDanger}  ||   Combo mAcc: {c.Red}{stat_combo_melee_accuracy} %{c.Default}")
    else:
        print(f"{tSafe}    ||   Combo mAcc: {stat_combo_melee_accuracy} %")

    # STATS END
    print(f"{c.bgDefault}{c.White}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return (
        stat_fkdr, stat_bw_kdr, stat_skywars_kdr, stat_bw_fksperstar, sumowlr,
        stat_sumo_bws, uhcwlr, uhckdr, wlr, stat_duels_wins,
        stat_duels_losses, stat_duels_bws, stat_melee_accuracy, stat_bedwars_star, nwl,
        stat_bblr, intswstar, bwstar, swstar, tDanger, tRisky, tSafe, stat_combo_melee_accuracy
    )

def em_requeue():
    keyboard.press('o')
    time.sleep(0.15)
    keyboard.release('o')
    time.sleep(0.1)
    print("Nebula > Emergency Dodge")
    keyboard.press('o')
    time.sleep(0.15)
    keyboard.release('o')
    time.sleep(0.5)
    print("Nebula > Emergency Dodge")
    keyboard.press('o')
    time.sleep(0.15)
    keyboard.release('o')
    time.sleep(1)
    print("Nebula > Emergency Dodge")
    keyboard.press('o')
    time.sleep(0.15)
    keyboard.release('o')
    time.sleep(1)
    print("Nebula > Emergency Dodge")
    print("Nebula > Dodged")
    time.sleep(0.5)
    print("Nebula > Requeuing in 5...")
    time.sleep(1)
    print("Nebula > Requeuing in 4...")
    time.sleep(1)
    print("Nebula > Requeuing in 3...")
    time.sleep(1)
    print("Nebula > Requeuing in 2...")
    time.sleep(1)
    print("Nebula > Requeuing in 1...")
    time.sleep(1)
    print("Nebula > Requeued")
    keyboard.press('p')
    time.sleep(0.15)
    keyboard.release('p')

def dodge():
    keyboard.press('o')
    time.sleep(0.15)
    keyboard.release('o')

    for i in range(requeue_delay, 0, -1):
        if not message_content.startswith("Woah there, slow down!"):
            time.sleep(1)
            print(Fore.MAGENTA + "Nebula > " + Fore.YELLOW + f"Requeuing in {i}..." + Style.RESET_ALL)
        else:
            em_requeue()

    if not message_content.startswith("Woah there, slow down!"):
        time.sleep(1)
        print(Fore.MAGENTA + "Nebula > " + Fore.YELLOW + "Requeued" + Style.RESET_ALL)
    else:
        em_requeue()

    keyboard.press('p')
    time.sleep(0.15)
    keyboard.release('p')
        
while True:
    try:
        message_list = chat.get_history(limit=3)

        # Check only the most recent message for spam
        last_message = message_list[-1]
        if last_message.content.startswith("Lilith > Found 1 likely nicked players"):
            print(Fore.RED + "Nebula > Found likely nicked player" + Style.RESET_ALL)
            if AutoDodge == True:
                if DodgeNicks == True:
                    dodge()
                else:
                    time.sleep(3)
            else:
                time.sleep(3)

        for message in message_list:
            message_content = message.content
            
            # Check if the message contains "Mystery Box!"
            if "Mystery Box!" not in message_content:
                ign = None  # initialize ign
                if message_content.startswith("?") and "W/L" not in message_content:
                    ign = message_content.split(" ")[1]
                    if ign.startswith("["):
                        ign = message_content.split(" ")[2]

                if ign:
                    if ign not in printed_igns or int(time.time()) - printed_igns[ign] >= 6.5:
                        printed_igns[ign] = int(time.time())
                        player_uuid = fetch_player_uuid(ign)
                        if player_uuid:
                            duels_wins, duels_losses, duels_winstreak, best_winstreak, overall_wins, overall_losses, \
                            overall_duels_winstreak, overall_best_winstreak, bedwars_wins, bedwars_losses, \
                            bedwars_winstreak, bedwars_final_kills, bedwars_final_deaths = fetch_player_stats(player_uuid)

                            if AntiSniper == True:
                                (
                                stat_fkdr, stat_bw_kdr, stat_skywars_kdr, stat_bw_fksperstar, sumowlr,
                                stat_sumo_bws, uhcwlr, uhckdr, wlr, stat_duels_wins,
                                stat_duels_losses, stat_duels_bws, stat_melee_accuracy, stat_bedwars_star, nwl,
                                stat_bblr, intswstar, bwstar, swstar, tDanger, tRisky, tSafe, stat_combo_melee_accuracy
                                ) = antisniper()

                            if ShowGamemode == True:
                                if duels_wins is not None and duels_losses is not None:
                                    win_ratio = calculate_ratio(duels_wins, duels_losses)
                                    print(Fore.WHITE + f"┣━━━━━━━━━━━━━━━━ {capgamemode} Duel")
                                    print(Fore.WHITE + f"┃ {ign} W: {duels_wins}, L: {duels_losses},")
                                    print(Fore.WHITE + f"┃ WLR: {win_ratio:.2f}, CWS: {duels_winstreak}, BWS: {best_winstreak}")
                                    if AntiSniper == True:
                                        if overall_wins is not None and overall_losses is not None:
                                            overall_ratio = calculate_ratio(overall_wins, overall_losses)
                                            print(Fore.WHITE + f"┣━━━━━━━━━━━━━━━━ Overall")
                                            print(Fore.WHITE + f"┃ {ign} W: {overall_wins}, L: {overall_losses},")
                                            print(Fore.WHITE + f"┃ WLR: {overall_ratio:.2f}, CWS: {overall_duels_winstreak}, BWS: {overall_best_winstreak}")
                                        else:
                                            print("┃ No overall stats found")

                                        if bedwars_wins is not None and bedwars_losses is not None:
                                            bedwars_ratio = calculate_ratio(bedwars_wins, bedwars_losses)
                                            try:
                                                print(Fore.WHITE + f"┣━━━━━━━━━━━━━━━━ Bedwars")
                                                print(Fore.WHITE + f"┃ {ign} ☆:{stat_bedwars_star}  W: {bedwars_wins}, L: {bedwars_losses}, WLR: {bedwars_ratio:.2f},")
                                                print(Fore.WHITE + f"┃ FKDR: {bedwars_final_kills / bedwars_final_deaths:.2f}, CWS: {bedwars_winstreak}, FK: {bedwars_final_kills}, FD: {bedwars_final_deaths}")
                                            except:
                                                print("┃ No bedwars stats found")
                                        else:
                                            print("┃ No bedwars stats found")
                                else:
                                    print("┃ No gamemode stats found")
                            else:
                                if AntiSniper == True:
                                    if overall_wins is not None and overall_losses is not None:
                                        overall_ratio = calculate_ratio(overall_wins, overall_losses)
                                        print(Fore.WHITE + f"┣━━━━━━━━━━━━━━━━ Overall")
                                        print(Fore.WHITE + f"┃ {ign} W: {overall_wins}, L: {overall_losses},")
                                        print(Fore.WHITE + f"┃ WLR: {overall_ratio:.2f}, CWS: {overall_duels_winstreak}, BWS: {overall_best_winstreak}")
                                    else:
                                        print("┃ No overall stats found")

                                    if bedwars_wins is not None and bedwars_losses is not None:
                                        bedwars_ratio = calculate_ratio(bedwars_wins, bedwars_losses)
                                        try:
                                            print(Fore.WHITE + f"┣━━━━━━━━━━━━━━━━ Bedwars")
                                            print(Fore.WHITE + f"┃ {ign} ☆:{stat_bedwars_star}  W: {bedwars_wins}, L: {bedwars_losses}, WLR: {bedwars_ratio:.2f},")
                                            print(Fore.WHITE + f"┃ FKDR: {bedwars_final_kills / bedwars_final_deaths:.2f}, CWS: {bedwars_winstreak}, FK: {bedwars_final_kills}, FD: {bedwars_final_deaths}")
                                        except:
                                            print("┃ No bedwars stats found")
                                    else:
                                        print("┃ No bedwars stats found")
                            try:
                                if (
                                    ign in dodge_igns
                                    or wlr > max_overall_wlr
                                    or duels_winstreak > max_current_ws
                                    or stat_duels_bws > max_best_ws
                                    or stat_fkdr > max_bedwars_fkdr
                                    or stat_bw_kdr > max_bedwars_kdr
                                    or stat_skywars_kdr > max_skywars_kdr
                                    or stat_bw_fksperstar > max_bedwars_finals_per_star
                                    or sumowlr > max_sumo_wlr
                                    or stat_sumo_bws > max_sumo_bws
                                    or nwl < min_network_level
                                    or uhcwlr > max_uhc_duels_wlr
                                    or uhckdr > max_uhc_kdr
                                    or stat_duels_wins < min_overall_wins
                                    or stat_duels_losses < min_overall_losses
                                    or stat_duels_bws > max_overall_bws
                                    or stat_melee_accuracy > max_melee_accuracy
                                    or stat_duels_bws == 0

                                    or duels_wins > max_wins
                                    or duels_wins < min_wins
                                    or duels_losses > max_losses
                                    or duels_losses < min_losses
                                    or win_ratio > max_wlr
                                    or win_ratio < min_wlr
                                    or duels_winstreak > max_current_ws
                                    or duels_winstreak < min_current_ws
                                    or best_winstreak > max_best_ws
                                    or best_winstreak < min_best_ws
                                ):
                                    if AutoDodge:
                                        print(Fore.RED + "┗━━━━━━━━━━━━━━━━ Dodged" + Style.RESET_ALL)
                                        dodge()
                                    else:
                                        print(Fore.RED + "┗━━━━━━━━━━━━━━━━ Sniper" + Style.RESET_ALL)
                                else:
                                    print(Fore.GREEN + "┗━━━━━━━━━━━━━━━━ Safe" + Style.RESET_ALL)
                                    

                            except Exception as e:
                                print(f"Exception occurred: {e}")
                                print(Fore.GREEN + "┗━━━━━━━━━━━━━━━━ Safe" + Style.RESET_ALL)
                                
    except Exception as e:
        continue

    time.sleep(0.1)