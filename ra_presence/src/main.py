import pygetwindow as gw
import psutil
import time
from api.ra_api import buscar_game_id, obter_detalhes_jogo
from core.constants import CONSOLE_MAP
from api.discord_rpc import DiscordRPC
from config import DISCORD_CLIENT_ID

ultimo_jogo_detectado = None
dados_cache = None
rpc = DiscordRPC(DISCORD_CLIENT_ID)
rpc.conectar()
tempo_sessao = None

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
        
        if info:
            if info['jogo'] != "Menu":
                if info['jogo'] != ultimo_jogo_detectado:
                    print(f"Novo jogo detectado: {info['jogo']}")
                    
                    console_id = CONSOLE_MAP.get(info['console'])
                    if console_id:
                        game_id = buscar_game_id(info['jogo'], console_id)
                        if game_id:
                            dados_cache = obter_detalhes_jogo(game_id)
                            ultimo_jogo_detectado = info['jogo']
                            tempo_sessao = time.time()
                    
                if dados_cache:
                    rpc.atualizar_status(
                        titulo=dados_cache['titulo'],
                        console=dados_cache['console'],
                        url_imagem=dados_cache['imagem'],
                        tempo_inicio=tempo_sessao
                    )
            else:
                if ultimo_jogo_detectado != "Menu":
                    rpc.limpar()
                    ultimo_jogo_detectado = "Menu"
                    print("No Menu do RALibRetro")
        else:
            if ultimo_jogo_detectado is not None:
                print("RALibRetro fechado.")
                rpc.limpar()
                ultimo_jogo_detectado = None

        time.sleep(15)