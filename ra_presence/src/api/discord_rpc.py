# ra_presence/src/api/discord_rpc.py
from pypresence import Presence

class DiscordRPC:
    def __init__(self, client_id):
        self.client_id = client_id
        self.rpc = Presence(client_id)
        self.conectado = False

    def conectar(self):
        try:
            self.rpc.connect()
            self.conectado = True
            print("Conectado ao Discord com Sucesso!")
        except Exception as e:
            print(f"[ERRO RPC] Falha ao conectar: {e}")

    # Novo parâmetro: texto_acao
    def atualizar_status(self, titulo, console, url_imagem, tempo_inicio, console_icon="saida", texto_acao="Jogando"):
        if not self.conectado:
            return

        try:
            self.rpc.update(
                details=f"{texto_acao} {titulo}", # <-- Usa o texto que você digitou no App
                state=console,
                large_image=url_imagem,
                large_text=titulo,
                small_image=console_icon,
                small_text=console,
                start=tempo_inicio
            )
        except Exception as e:
            print(f"[ERRO RPC Interno] Falha ao atualizar: {e}")

    def limpar(self):
        if self.conectado:
            self.rpc.clear()