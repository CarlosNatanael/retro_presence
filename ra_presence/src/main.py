import psutil
import time
from api.ra_api import obter_detalhes_jogo, obter_jogo_atual
from api.discord_rpc import DiscordRPC
from config import DISCORD_CLIENT_ID

# --- VARIÁVEIS DE CONTROLE ---
ultimo_game_id = None
dados_cache = None
tempo_sessao = None

# Inicializa o RPC
rpc = DiscordRPC(DISCORD_CLIENT_ID)
rpc.conectar()

if __name__ == "__main__":
    print("\n" + "="*40)
    print("SISTEMA DE MONITORIZAÇÃO COM DEBUG AVANÇADO")
    print("="*40 + "\n")
    
    while True:
        # --- DEBUG DE PROCESSOS ---
        processos_encontrados = [p.name() for p in psutil.process_iter() if "ralibretro" in p.name().lower() or "code" in p.name().lower()]
        
        emulador_aberto = any("ralibretro" in p.lower() for p in processos_encontrados)
        vscode_aberto = any("code" in p.lower() for p in processos_encontrados)

        if emulador_aberto:
            print(f"[DEBUG] RALibRetro detectado! (Outros processos ativos: {processos_encontrados})")
            
            game_id = obter_jogo_atual()

            if game_id and game_id != ultimo_game_id:
                print(f"[RA] Mudança de jogo! Novo ID: {game_id}")
                detalhes = obter_detalhes_jogo(game_id)
                if detalhes:
                    dados_cache = detalhes
                    ultimo_game_id = game_id
                    tempo_sessao = time.time()
                else:
                    print(f"[ERRO] Falha ao buscar detalhes do ID {game_id}")

            if dados_cache:
                print(f"[RPC] Enviando atualização para o Discord: {dados_cache['titulo']}")
                try:
                    rpc.atualizar_status(
                        titulo=dados_cache['titulo'],
                        console=dados_cache['console'],
                        url_imagem=dados_cache['imagem'],
                        tempo_inicio=tempo_sessao
                    )
                except Exception as e:
                    print(f"[ERRO RPC] Falha ao enviar para o Discord: {e}")
        else:
            if ultimo_game_id is not None:
                print("[STATUS] RALibRetro fechado. Limpando presença...")
                rpc.limpar()
                ultimo_game_id = None
                dados_cache = None
            else:
                print("[IDLE] RALibRetro não encontrado. Aguardando...")

        time.sleep(15)