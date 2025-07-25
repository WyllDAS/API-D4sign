from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from DocModelPDF import *
import pyautogui as py
import subprocess  # adicione no topo com os outros imports


# Cores padrão do tema escuro
BG_COLOR = "#121212"
FG_COLOR = "#FFFFFF"
ACCENT_COLOR = "#003366"
BTN_HOVER_COLOR = "#005599"

arquivo = ""
diretorio = ""
linha_inicio = None
linha_fim = None
label_arquivo = None
label_diretorio = None
campos_completos = False

def atualizar_botaoRodar():
    if arquivo and diretorio:
        botaoRodar.config(state="normal")
    else:
        botaoRodar.config(state="disabled")

def selecionar_arquivo():
    global arquivo, label_arquivo
    arquivo = filedialog.askopenfilename(
        title="Selecionar arquivo Excel",
        filetypes=(("Arquivos Excel", "*.xlsx;*.xls"), ("Todos os arquivos", "*.*"))
    )
    if arquivo:
        label_arquivo.config(text=f"📄 Arquivo Selecionado: {arquivo}")
    atualizar_botaoRodar()

def selecionar_pasta():
    global diretorio, label_diretorio
    diretorio = filedialog.askdirectory(title="Selecione a pasta para salvar o relatório")
    if diretorio:
        label_diretorio.config(text=f"📁 Pasta Selecionada: {diretorio}")
    atualizar_botaoRodar()

def selecionar_linhas():
    def confirmar_linhas():
        nonlocal entrada_inicio, entrada_fim
        try:
            inicio = int(entrada_inicio.get())
            fim = int(entrada_fim.get())
            if inicio > fim:
                raise ValueError("A linha inicial não pode ser maior que a final.")
            global linha_inicio, linha_fim
            linha_inicio = inicio
            linha_fim = fim
            messagebox.showinfo("Linhas Definidas", f"Linha inicial: {linha_inicio}\nLinha final: {linha_fim}")
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    janela_linhas = Toplevel(root)
    janela_linhas.title("Definir Intervalo de Linhas")
    janela_linhas.configure(bg=BG_COLOR)
    
    ttk.Label(janela_linhas, text="Linha Inicial:").grid(row=0, column=0, padx=10, pady=10)
    entrada_inicio = ttk.Entry(janela_linhas, width=10)
    entrada_inicio.grid(row=0, column=1)

    ttk.Label(janela_linhas, text="Linha Final:").grid(row=1, column=0, padx=10, pady=10)
    entrada_fim = ttk.Entry(janela_linhas, width=10)
    entrada_fim.grid(row=1, column=1)

    ttk.Button(janela_linhas, text="Confirmar", command=confirmar_linhas).grid(row=2, column=0, columnspan=2, pady=15)

def rodarRobo():
    criar_proposta(arquivo, diretorio, linha_inicio, linha_fim)
    py.alert('FINALIZADO')

def set_style(root):
    style = ttk.Style(root)
    root.configure(bg=BG_COLOR)
    style.theme_use('clam')
    style.configure('TFrame', background=BG_COLOR)
    style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=('Segoe UI', 11))
    style.configure('TButton', background=ACCENT_COLOR, foreground=FG_COLOR, font=('Segoe UI', 10, 'bold'))
    style.map('TButton', background=[('active', BTN_HOVER_COLOR), ('!active', ACCENT_COLOR)])
    style.configure('TEntry', fieldbackground=BG_COLOR, foreground=FG_COLOR)
def executar_envio():
    try:
        subprocess.Popen(["python", "janela1.py"], shell=True)
        # Para executar como administrador (opcional, Windows):
        # subprocess.run(['powershell', '-Command', 'Start-Process python -ArgumentList "janela1.py" -Verb RunAs'], shell=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível executar o script de envio:\n{e}")
def criar_interface():
    global root, botaoRodar, label_arquivo, label_diretorio
    root = Tk()
    root.title('Automação de Propostas')
    root.state('zoomed')
    root.iconbitmap('icon.ico')

    set_style(root)

    # Frame topo: imagem centralizada, título e botões no canto superior direito
    frame_topo = ttk.Frame(root)
    frame_topo.pack(fill=X, padx=20, pady=10)

    frame_topo.columnconfigure(0, weight=1)
    frame_topo.columnconfigure(1, weight=2)
    frame_topo.columnconfigure(2, weight=1)

    # Imagem
    imagem = Image.open("Logo.png").resize((160, 160), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(imagem)
    imagem_label = ttk.Label(frame_topo, image=image_tk)
    imagem_label.image = image_tk
    #imagem_label.grid(row=0, column=1, pady=(0,10))
    imagem_label.grid(row=0, column=0, sticky="w")

    # Título
    titulo = ttk.Label(frame_topo, text="PROPOSTAS - PROJETO S", font=("Segoe UI", 16, "bold"))
    titulo.grid(row=0, column=1, pady=(0,10))

    # Botões topo direito (envio, sair)
    frame_botoes_direita = ttk.Frame(frame_topo)
    frame_botoes_direita.grid(row=0, column=3, sticky="ne", padx=10, pady=5)
    ttk.Button(frame_botoes_direita, text="📨 Envio", command=executar_envio).pack(side=LEFT, padx=5)
    ttk.Button(frame_botoes_direita, text="🚪 Sair", command=root.destroy).pack(side=LEFT, padx=5)

    # --- NOVO FRAME para os botões funcionais, logo abaixo do frame_topo ---
    frame_botoes_funcionais = ttk.Frame(root)
    frame_botoes_funcionais.pack(pady=20)

    # Organiza em grid para alinhar direito (ajuste colunas conforme precisar)
    frame_botoes_funcionais.columnconfigure((0,1,2,3), weight=1)

    ttk.Button(frame_botoes_funcionais, text="Selecionar Arquivo Excel", command=selecionar_arquivo)\
        .grid(row=0, column=0, padx=10)
    ttk.Button(frame_botoes_funcionais, text="Selecionar Pasta", command=selecionar_pasta)\
        .grid(row=0, column=1, padx=10)
    ttk.Button(frame_botoes_funcionais, text="Definir Linhas", command=selecionar_linhas)\
        .grid(row=0, column=2, padx=10)

    botaoRodar = ttk.Button(frame_botoes_funcionais, text="▶ START", command=rodarRobo, state=DISABLED)
    botaoRodar.grid(row=0, column=3, padx=10)

    label_arquivo = ttk.Label(root, text="📄 Nenhum arquivo selecionado")
    label_arquivo.pack(pady=10)

    label_diretorio = ttk.Label(root, text="📁 Nenhuma pasta selecionada")
    label_diretorio.pack(pady=10)

    rodape = ttk.Label(root, text="Todos os direitos reservados © - INNOV - 2025", anchor="center")
    rodape.pack(side="bottom", fill="x", pady=10)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()
