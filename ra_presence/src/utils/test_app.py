import psutil

def listar_processos():
    try:
        print(f"{'PID':<10} {'Nome do Processo'}")
        print("-" * 40)
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            pid = proc.info['pid']
            nome = proc.info['name'] or "Desconhecido"
            print(f"{pid:<10} {nome}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    except Exception as e:
        print(f"Erro ao listar processos: {e}")

if __name__ == "__main__":
    listar_processos()
