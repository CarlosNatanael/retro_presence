import sys
import os
import psutil
import time
import threading
import customtkinter as ctk
from api.ra_api import obter_detalhes_jogo, obter_jogo_atual
from api.discord_rpc import DiscordRPC
from core.constants import DISCORD_CONSOLE_ASSETS
from config import DISCORD_CLIENT_ID

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

rpc = DiscordRPC(DISCORD_CLIENT_ID)

class RetroPresenceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RA Discord Presence")
        self.geometry("450x520")
        self.resizable(False, False)
        
        caminho_icone = resource_path(os.path.join("assets", "icone.ico"))
        try:
            self.iconbitmap(caminho_icone)
        except Exception:
            pass
            
        self.monitorando = False
        self.ultimo_game_id = None
        self.tempo_sessao = None

        self.label_status = ctk.CTkLabel(self, text="Status: Aguardando...", text_color="gray", font=("Arial", 14, "bold"))
        self.label_status.pack(pady=(15, 5))
        
        self.label_acao = ctk.CTkLabel(self, text="Primeira linha (Ex: Jogando, Desenvolvendo):")
        self.label_acao.pack(pady=(5, 0))
        
        self.entrada_acao = ctk.CTkEntry(self, width=250)
        self.entrada_acao.insert(0, "Jogando")
        self.entrada_acao.pack(pady=5)

        self.label_estado = ctk.CTkLabel(self, text="Segunda linha (Vazio = Console):")
        self.label_estado.pack(pady=(5, 0))
        
        self.entrada_estado = ctk.CTkEntry(self, width=250)
        self.entrada_estado.insert(0, "") # Começa vazio
        self.entrada_estado.pack(pady=5)
        
        self.btn_toggle = ctk.CTkButton(self, text="Iniciar Monitoramento", command=self.toggle_monitor)
        self.btn_toggle.pack(pady=10)
        
        self.caixa_log = ctk.CTkTextbox(self, width=400, height=180, state="disabled")
        self.caixa_log.pack(pady=(10, 15))
        
        self.log("Aplicativo iniciado. Aguardando comando.")

    def log(self, mensagem):
        self.after(0, self._inserir_log, mensagem)

    def _inserir_log(self, mensagem):
        hora_atual = time.strftime("%H:%M:%S")
        self.caixa_log.configure(state="normal")
        self.caixa_log.insert("end", f"[{hora_atual}] {mensagem}\n")
        self.caixa_log.see("end")
        self.caixa_log.configure(state="disabled")

    def toggle_monitor(self):
        if not self.monitorando:
            self.monitorando = True
            self.btn_toggle.configure(text="Parar Monitoramento", fg_color="red", hover_color="#8B0000")
            self.label_status.configure(text="Status: Conectando...", text_color="yellow")
            
            try:
                rpc.conectar()
                self.log("Conectado ao DiscordRPC com sucesso.")
            except Exception as e:
                self.log(f"Erro ao conectar no Discord: {e}")
            
            threading.Thread(target=self.loop_monitoramento, daemon=True).start()
        else:
            self.monitorando = False
            self.btn_toggle.configure(text="Iniciar Monitoramento", fg_color=["#3B8ED0", "#1F6AA5"])
            self.label_status.configure(text="Status: Parado", text_color="gray")
            rpc.limpar()
            self.ultimo_game_id = None
            self.log("Monitoramento interrompido. Discord limpo.")

    def loop_monitoramento(self):
        self.label_status.configure(text="Status: Monitorando RALibretro...", text_color="green")
        self.log("Procurando pelo emulador...")
        
        while self.monitorando:
            processos_encontrados = [p.name() for p in psutil.process_iter() if "ralibretro" in p.name().lower() or "code" in p.name().lower()]
            emulador_aberto = any("ralibretro" in p.lower() for p in processos_encontrados)

            if emulador_aberto:
                game_id = obter_jogo_atual()
                
                if game_id:
                    acao_atual = self.entrada_acao.get()
                    estado_atual = self.entrada_estado.get()
                    mudou_texto = (not hasattr(self, 'ultima_acao') or self.ultima_acao != acao_atual or
                                   not hasattr(self, 'ultimo_estado') or self.ultimo_estado != estado_atual)
                    
                    if game_id != self.ultimo_game_id or mudou_texto:
                        detalhes = obter_detalhes_jogo(game_id)
                        
                        if detalhes:
                            if game_id != self.ultimo_game_id:
                                self.log(f"Jogo detectado: {detalhes['titulo']} ({detalhes['console']})")
                                self.tempo_sessao = time.time()
                                
                            self.ultimo_game_id = game_id
                            self.ultima_acao = acao_atual
                            self.ultimo_estado = estado_atual
                            
                            icone_curto = DISCORD_CONSOLE_ASSETS.get(detalhes['console'], "unknown")
                            url_icone_console = f"https://static.retroachievements.org/assets/images/system/{icone_curto}.png"
                            
                            log_estado = estado_atual if estado_atual.strip() else detalhes['console']
                            self.log(f"Discord atualizado -> {acao_atual} {detalhes['titulo']} | {log_estado}")
                            
                            rpc.atualizar_status(
                                titulo=detalhes['titulo'],
                                console=detalhes['console'],
                                url_imagem=detalhes['imagem'],
                                tempo_inicio=self.tempo_sessao,
                                console_icon=url_icone_console,
                                texto_acao=acao_atual,
                                texto_estado=estado_atual
                            )
            else:
                if self.ultimo_game_id is not None:
                    self.log("Emulador fechado. Limpando status...")
                    rpc.limpar()
                    self.ultimo_game_id = None
                    self.tempo_sessao = None

            time.sleep(15)

if __name__ == "__main__":
    app = RetroPresenceApp()
    app.mainloop()