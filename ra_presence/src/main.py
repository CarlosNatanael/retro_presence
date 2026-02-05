import pygetwindow as gw
import psutil
import time
from api.ra_api import obter_detalhes_jogo, obter_jogo_atual
from core.constants import CONSOLE_MAP
from api.discord_rpc import DiscordRPC
from config import DISCORD_CLIENT_ID

ultimo_game_id = None
dados_cache = None
tempo_sessao = None

rpc = DiscordRPC(DISCORD_CLIENT_ID)
rpc.conectar()

if __name__ == "__main__":
    print("\n" + "="*40)
    print("SISTEMA DE MONITORIZAÇÃO ATIVO (VIA PERFIL RA)")
    print("="*40 + "\n")
    
    while True:
        emulador_aberto = any("ralibretro" in p.name().lower() for p in psutil.process_iter())
        if emulador_aberto:
            game_id = obter_jogo_atual()
            if game_id and game_id != ultimo_game_id:
                print(f"[RA] Novo jogo detectado no seu perfil: ID {game_id}")
                
                detalhes = obter_detalhes_jogo(game_id)
                if detalhes:
                    dados_cache = detalhes
                    ultimo_game_id = game_id
                    tempo_sessao = time.time()
                    print(f"[STATUS] Jogando agora: {dados_cache['titulo']}\n")
                else:
                    print(f"[ERRO] Não foi possível carregar detalhes do ID {game_id}")

            if dados_cache:
                rpc.atualizar_status(
                    titulo=dados_cache['titulo'],
                    console=dados_cache['console'],
                    url_imagem=dados_cache['imagem'],
                    tempo_inicio=tempo_sessao
                )
        else:
            if ultimo_game_id is not None:
                print("[STATUS] Emulador fechado. Limpando presença no Discord...")
                rpc.limpar()
                ultimo_game_id = None
                dados_cache = None
        time.sleep(15)