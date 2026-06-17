import psutil
import time
from api.ra_api import obter_detalhes_jogo, obter_jogo_atual
from api.discord_rpc import DiscordRPC
from core.constants import DISCORD_CONSOLE_ASSETS
from config import DISCORD_CLIENT_ID

ultimo_game_id = None
tempo_sessao = None

rpc = DiscordRPC(DISCORD_CLIENT_ID)
rpc.conectar()

if __name__ == "__main__":
    print("[*] Iniciando monitoramento leve do RALibretro...")
    
    while True:
        processos_encontrados = [p.name() for p in psutil.process_iter() if "ralibretro" in p.name().lower() or "code" in p.name().lower()]
        emulador_aberto = any("ralibretro" in p.lower() for p in processos_encontrados)

        if emulador_aberto:
            game_id = obter_jogo_atual()
            
            if game_id and game_id != ultimo_game_id:
                print(f"\n[RA] Novo jogo detectado! ID: {game_id}")
                detalhes = obter_detalhes_jogo(game_id)
                
                if detalhes:
                    ultimo_game_id = game_id
                    tempo_sessao = time.time()
                    
                    # 1. Pega o nome curto do dicionário (ex: 'dc', 'snes')
                    icone_curto = DISCORD_CONSOLE_ASSETS.get(detalhes['console'], "unknown")
                    
                    # 2. Monta a URL mágica do RetroAchievements!
                    url_icone_console = f"https://static.retroachievements.org/assets/images/system/{icone_curto}.png"
                    
                    print(f"[RPC] Atualizando: {detalhes['titulo']} ({detalhes['console']})")
                    
                    rpc.atualizar_status(
                        titulo=detalhes['titulo'],
                        console=detalhes['console'],
                        url_imagem=detalhes['imagem'],
                        tempo_inicio=tempo_sessao,
                        console_icon=url_icone_console  # <-- Enviando a URL pronta!
                    )
        else:
            if ultimo_game_id is not None:
                print("[STATUS] Emulador fechado. Limpando Discord...")
                rpc.limpar()
                ultimo_game_id = None
                tempo_sessao = None

        time.sleep(15)