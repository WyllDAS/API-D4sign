from tkinter import * 
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from DocModelPDF import *
import pyautogui as py


arquivo = ""
diretorio = ""
linha_inicio = None
linha_fim = None
frame_topo= None
botao_selecionar = None
botao = None
label_arquivo = None
label_diretorio = None
campos_completos = False

def atualizar_botaoRodar():
    global campos_completos,botaoRodar 
    if arquivo and diretorio:
        botaoRodar.config(state="normal",bg="green",fg='black',font=("Segoe UI", 10, "bold"))
        campos_completos = True
    else:
        botaoRodar.config(state="disabled",bg="red",fg='blue',font=("Segoe UI", 10, "bold"))
        campos_completos=False
def selecionar_arquivo():
    global arquivo,label_arquivo
    # Label para mostrar o arquivo selecionado
    if label_arquivo:
        label_arquivo.pack_forget()
    label_arquivo = Label(root, text="Nenhum arquivo selecionado", font=("Segoe UI", 14))
    label_arquivo.pack(side=TOP,pady=10)  # Centralizar label
    arquivo = filedialog.askopenfilename(
        title="Selecionar arquivo excel",
        filetypes=(("Arquivos Excel", "*.xlsx;*.xls"), ("Todos os arquivos", "*.*"))
    )
    if arquivo:
        label_arquivo.config(text=f"Arquivo Selecionado {arquivo}",font=("Segoe UI", 12))
    atualizar_botaoRodar()
def selecionar_pasta():
    global diretorio,label_diretorio
    if label_diretorio:
        label_diretorio.pack_forget()
    label_diretorio = Label(root, text="Nenhuma pasta selecionada", font=("Segoe UI", 14))
    label_diretorio.pack(pady=20)
    diretorio = filedialog.askdirectory(title="Selecione a pasta para salvar o relatório")
    if diretorio:
        label_diretorio.config(text=f"Pasta selecionada: {diretorio}",font=("Segoe UI", 12))
    atualizar_botaoRodar()

def selecionar_linhas():
    global linha_inicio, linha_fim
    if label_arquivo:
        label_arquivo.pack_forget()
    elif label_diretorio:
        label_diretorio.pack_forget()
     # Cria um novo frame só para os campos de linha
    frame_linhas = Frame(root)
    frame_linhas.pack(pady=10)

    # Linha Inicial
    label_inicio = Label(frame_linhas, text="Linha Inicial:", font=("Segoe UI", 10))
    label_inicio.grid(row=0, column=0, padx=5, pady=5)
    entrada_inicio = Entry(frame_linhas, width=10)
    entrada_inicio.grid(row=0, column=1, padx=5)

    # Linha Final
    label_fim = Label(frame_linhas, text="Linha Final:", font=("Segoe UI", 10))
    label_fim.grid(row=0, column=2, padx=5, pady=5)
    entrada_fim = Entry(frame_linhas, width=10)
    entrada_fim.grid(row=0, column=3, padx=5)

    def confirmar_linhas():
        global linha_inicio, linha_fim
        try:
            inicio = int(entrada_inicio.get())
            fim = int(entrada_fim.get())
            if inicio > fim:
                raise ValueError("A linha inicial não pode ser maior que a final.")
            linha_inicio = inicio
            linha_fim = fim
            messagebox.showinfo("Linhas Definidas", f"Linha inicial: {linha_inicio}\nLinha final: {linha_fim}")
            print(linha_inicio, linha_fim)  # Aqui, depois de definir as linhas
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    botao_confirmar = Button(frame_linhas, text="Confirmar", command=confirmar_linhas)
    botao_confirmar.grid(row=1, column=1, columnspan=2, pady=10)  # Ajuste para o botão


def rodarRobo():
    criar_proposta(arquivo, diretorio,linha_inicio,linha_fim)
    py.alert('FINALIZADO')
    



def criar_interface():
    global root, botao_selecionar, botao, label_arquivo,label_diretorio,botaoRodar
    root = Tk()
    root.title('Automação')
    root.iconbitmap('icon.ico')
    
    # Definindo o tamanho da janela
    root.state('zoomed')
    
    # Carregar imagem
    imagem = Image.open("Logo.png")
    imagem = imagem.resize((160, 160), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(imagem)
    
    # Label para imagem (centralizado)
    imagem_label = Label(root, image=image_tk)
    imagem_label.pack(pady=20)  # Centralizar imagem com espaçamento
    
    # Título (centralizado)
    titulo = Label(root, text="PROPOSTAS - PROJETO S", font=("Segoe UI", 16))
    titulo.pack(pady=10)  # Centralizar título com espaçamento


    #criar frame
    frame_topo = Frame(root)
    frame_topo.pack(pady=20)

    
    # Botão para selecionar o arquivo Excel
    botao_selecionar = Button(frame_topo, text="Selecionar Arquivo Excel", command=selecionar_arquivo)
    botao_selecionar.grid(row=0, column=0, padx=20)  # Centralizar botão com espaçamento

    # Botão para selecionar o diretorio
    botao_dire = Button(frame_topo, text="Selecionar pasta", command=selecionar_pasta)
    botao_dire.grid(row=0, column=1, padx=20)  # Centralizar botão com espaçamento

    #botao para index
    botao_index = Button(frame_topo,text="Definir linhas",command=selecionar_linhas)
    botao_index.grid(row=0,column=2,pady=20)

    #botao automacao
    botaoRodar = Button(frame_topo,text="START",command=rodarRobo)
    botaoRodar.grid(row=0, column=7, pady=60)
    botaoRodar.config(state=DISABLED,bg="red",fg='blue',font=("Segoe UI", 10, "bold"))
    

    

    rodape = Label(root, text="Todos os direitos reservados © - SEIN - 2025", font=("Segoe UI", 10))
    rodape.config(bg="#D3D3D3", relief=SUNKEN)  # Cor de fundo neutra (cinza claro) e borda inferior
    rodape.pack(side="bottom", fill="x", pady=10)
    root.mainloop()

if __name__ == "__main__":
    criar_interface()
