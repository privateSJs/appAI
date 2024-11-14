import os
import sys
import subprocess


# Krok 1: Tworzenie wirtualnego środowiska .venv, jeśli nie istnieje
if not os.path.exists(".venv"):
    print("Tworzenie wirtualnego środowiska .venv...")
    subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
    print("Wirtualne środowisko .venv zostało utworzone.")

# Krok 2: Instalacja zależności w .venv
print("Instalacja zależności w środowisku .venv...")
pip_path = os.path.join(".venv", "Scripts", "pip") if os.name == "nt" else os.path.join(".venv", "bin", "pip")
subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
print("Zainstalowano pomyślnie zależności.")

# Krok 3: Uruchomienie aplikacji tkinter w kontekście wirtualnego środowiska
python_path = os.path.join(".venv", "Scripts", "python") if os.name == "nt" else os.path.join(".venv", "bin", "python")
subprocess.check_call([python_path, "-m", "utils.installer"])