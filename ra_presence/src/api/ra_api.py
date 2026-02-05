import requests
from config import RA_USER, RA_API_KEY

def obter_jogo_atual():
    url = f"https://retroachievements.org/API/API_GetUserSummary.php?z={RA_USER}&y={RA_API_KEY}&u={RA_USER}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        last_game_id = data.get('LastGameID')
        if last_game_id and int(last_game_id) != 0:
            return last_game_id
            
    except Exception as e:
        print(f"[ERRO API] Falha ao ler resumo do usuário: {e}")
    return None

def obter_detalhes_jogo(game_id):
    url = f"https://retroachievements.org/API/API_GetGameInfoAndUserProgress.php?z={RA_USER}&y={RA_API_KEY}&g={game_id}&u={RA_USER}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        image_path = data.get('ImageIcon') 
        
        return {
            "titulo": data.get('Title'),
            "imagem": f"https://media.retroachievements.org{image_path}" if image_path else None,
            "console": data.get('ConsoleName')
        }
    except Exception as e:
        print(f"[ERRO API] Falha ao obter detalhes: {e}")
        return None