import pygetwindow as gw
import psutil
import time
from api.ra_api import buscar_game_id, obter_detalhes_jogo
from core.constants import CONSOLE_MAP

ultimo_jogo_detectado = None
dados_cache = None

def buscar_jogo_no_titulo():
    processo_ativo = any("RALibRetro.exe" in p.name() for p in psutil.process_iter())
    if not processo_ativo: return None
    
    todas_janelas = gw.getWindowsWithTitle('RALibRetro')
    if not todas_janelas: return {"jogo": "Menu", "console": None}
    
    titulo = todas_janelas[0].title
    partes = titulo.split(" - ")
    
    if len(partes) >= 5:
        return {"jogo": partes[4], "console": partes[3]}
    return {"jogo": "Menu", "console": None}

if __name__ == "__main__":
    print("Iniciando monitoramento... (Crtl+C para parar)")
    
    while True:
        info = buscar_jogo_no_titulo()
        
        if info and info['jogo'] != "Menu":
            if info['jogo'] != ultimo_jogo_detectado:
                print(f"Novo jogo detectado: {info['jogo']}. Buscando dados no RA...")
                
                console_id = CONSOLE_MAP.get(info['console'])
                if console_id:
                    game_id = buscar_game_id(info['jogo'], console_id)
                    if game_id:
                        dados_cache = obter_detalhes_jogo(game_id)
                        ultimo_jogo_detectado = info['jogo']
                        print(f"Dados carregados: {dados_cache['titulo']} ({dados_cache['console']})")
                    else:
                        print("Jogo não encontrado na base do RA.")
                else:
                    print(f"Console '{info['console']}' não mapeado em constants.py")

            if dados_cache:
                print(f"Rich Presence Ativo: {dados_cache['titulo']} | Imagem: {dados_cache['imagem']}")
        
        elif info and info['jogo'] == "Menu":
            print("RALibRetro aberto, mas nenhum jogo carregado.")
            ultimo_jogo_detectado = None
            dados_cache = None

        time.sleep(15)