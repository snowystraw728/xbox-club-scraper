import re
import requests
import json
from colorama import Fore, Style, init

init(autoreset=True)

def extract_player_xuids(data):
    player_xuids = []
    for club in data.get("clubs", []):
        club_presence = club.get("clubPresence", [])
        for presence in club_presence:
            xuid = presence.get("xuid")
            if xuid:
                player_xuids.append(xuid)
    return player_xuids

club_id = input(f"{Fore.RED}Enter Club ID: {Fore.BLUE}")
authorization_token = input(f"{Fore.RED}Enter Authorization Token: {Fore.BLUE}")

headers = {
    'x-xbl-contract-version': '2',
    'Authorization': authorization_token,
    'Accept-Language': 'en_us'
}

base_url = f"https://clubhub.xboxlive.com/clubs/Ids({club_id})/decoration/clubpresence"
response = requests.get(base_url, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    player_xuids = extract_player_xuids(data)

    next_link = data.get("nextLink")
    while next_link:
        response = requests.get(next_link, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.text)
            player_xuids += extract_player_xuids(data)
            next_link = data.get("nextLink")
        else:
            print(f"Error: Status code {response.status_code}")
            break

    with open(f"xuids.club.{club_id}.txt", "w", encoding="utf-8") as file:
        for xuid in player_xuids:
            file.write(xuid + "\n")

    print(f"{Fore.GREEN}XUIDs saved to xuids.club.{club_id}.txt{Style.RESET_ALL}")
else:
    print(f"{Fore.RED} Error: Status code {response.status_code}")
