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

    def atualizar_status(self, titulo, console, url_imagem, tempo_inicio, console_icon="saida"):
        if not self.conectado:
            return

        try:
            self.rpc.update(
                details=f"Jogando {titulo}",
                state=console,
                large_image=url_imagem, # <-- Volta a URL do jogo para cá
                large_text=titulo,
                small_image=console_icon, # <-- O ícone do console volta para cá
                small_text=console,
                start=tempo_inicio
            )
        except Exception as e:
            print(f"[ERRO RPC Interno] Falha ao atualizar: {e}")

    def limpar(self):
        if self.conectado:
            self.rpc.clear()