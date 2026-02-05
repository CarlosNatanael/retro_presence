from pypresence import Presence
import time

class DiscordRPC:
    def __init__(self, cliente_id):
        self.rpc = Presence(cliente_id)
        self.conectado = False

    def conectar(self):
        try:
            self.rpc.connect()
            self.conectado = True
            print("Conectado ao Discord com Sucesso!")
        except Exception as e:
            print(f"Erro ao conectar ao Discord: {e}")

    def atualizar_status(self, titulo, console, url_imagem, tempo_inicio):
        if not self.conectado:
            return
        
        self.rpc.update(
            details=f"Jogando {titulo}",
            state=console,
            large_image=url_imagem,
            large_text=titulo,
            small_image="ralibretro_logo",
            small_text="RALibRetro Emulator",
            start=tempo_inicio
        )

    def limpar(self):
        self.rpc.clear()