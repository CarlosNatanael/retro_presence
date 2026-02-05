import requests
import os
from config import RA_USER, RA_API_KEY

def buscar_game_id(nome_jogo, console_id):
    url = f"https://ra.api.retroachievements.org/API/API_GetGameList.php?z={RA_USER}&y={RA_API_KEY}&i={console_id}"
    response = requests.get(url).json()
    
    for game in response:
        if nome_jogo.lower() in game['Title'].lower():
            return game['ID']
    return None

def obter_detalhes_jogo(game_id):
    url = f"https://ra.api.retroachievements.org/API/API_GetGame.php?z={RA_USER}&y={RA_API_KEY}&i={game_id}"
    data = requests.get(url).json()
    return {
        "titulo": data['Title'],
        "imagem": f"https://media.retroachievements.org{data['ImageIconPath']}",
        "console": data['ConsoleName']
    }