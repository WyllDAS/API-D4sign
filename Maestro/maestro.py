import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

# Cores do tema escuro
BG_COLOR = "#121212"
FG_COLOR = "#FFFFFF"
ACCENT_COLOR = "#003366"
BTN_HOVER_COLOR = "#005599"

# Caminhos dos scripts (ajuste se necessário)
SCRIPT_CONTRATOS = "proposta-app1.py"
SCRIPT_ENVIO = "janela1.py"

def set_style(root):
    style = ttk.Style(root)
    root.configure(bg=BG_COLOR)
    style.theme_use('clam')
    style.configure('TFrame', background=BG_COLOR)
    style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=('Segoe UI', 14, 'bold'))
    style.configure('TButton', background=ACCENT_COLOR, foreground=FG_COLOR, font=('Segoe UI', 12, 'bold'), padding=10)
    style.map('TButton', background=[('active', BTN_HOVER_COLOR), ('!active', ACCENT_COLOR)])

def run_script_as_admin(script_path):
    try:
        script_full = os.path.abspath(script_path)
        if not os.path.exists(script_full):
            messagebox.showerror("Erro", f"Script não encontrado:\n{script_full}")
            return

        # Executa como administrador (Windows)
        subprocess.run(
            ['powershell','-WindowStyle','Hidden', '-Command', f'Start-Process python -ArgumentList "{script_full}" -Verb RunAs'],
            shell=True
        )
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao executar {script_path}:\n{e}")

def criar_interface():
    root = tk.Tk()
    root.title("Sistema Central de Automação")
    root.geometry("600x400")
    root.resizable(False, False)
    set_style(root)

    frame = ttk.Frame(root)
    frame.pack(expand=True)

    ttk.Label(frame, text="Escolha a funcionalidade:", font=("Segoe UI", 16)).pack(pady=30)

    ttk.Button(frame, text="📄 CONTRATOS", command=lambda: run_script_as_admin(SCRIPT_CONTRATOS)).pack(pady=20, ipadx=20)
    ttk.Button(frame, text="📨 ENVIO", command=lambda: run_script_as_admin(SCRIPT_ENVIO)).pack(pady=20, ipadx=30)

    ttk.Label(root, text="© INNOV - 2025", font=("Segoe UI", 10)).pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()
