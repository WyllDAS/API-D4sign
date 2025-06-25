import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from main import Assinaturas  # sua classe Assinaturas já implementada com os métodos
import requests

# Cores da empresa
BG_COLOR = "#121212"          # preto quase total
FG_COLOR = "#FFFFFF"          # branco puro
ACCENT_COLOR = "#003366"      # azul escuro vibrante
BTN_HOVER_COLOR = "#005599"   # azul hover mais claro

# Token e cryptKey fixos (coloque os seus aqui)
TOKEN = 'live_06af34ccfb4af78705087108c672fcd083608e3e6ff31bdb5a01305de5600826'
CRYPTKEY = 'live_crypt_7xNn4VIDjbL1Ko0rI7dqd0xBBMROHYOf'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("D4Sign Gerenciador")
        self.state('zoomed')  # inicia maximizado
        self.configure(bg=BG_COLOR)

        self.style = ttk.Style(self)
        self.set_style()

        self.assinador = Assinaturas(TOKEN, CRYPTKEY)
        self.assinador.listar_cofres()

        self.create_widgets()
        self.atualizar_cofres()

    def set_style(self):
        self.style.theme_use('clam')

        self.style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=('Helvetica', 12, 'bold'))
        self.style.configure('TFrame', background=BG_COLOR)
        self.style.configure('TLabelframe', background=BG_COLOR, foreground=ACCENT_COLOR, font=('Helvetica', 14, 'bold'))
        self.style.configure('TLabelframe.Label', background=BG_COLOR, foreground=ACCENT_COLOR, font=('Helvetica', 15, 'bold'))

        self.style.configure('TCombobox',
                             fieldbackground=BG_COLOR,
                             background=BG_COLOR,
                             foreground=FG_COLOR,
                             selectbackground=ACCENT_COLOR,
                             selectforeground=FG_COLOR,
                             arrowcolor=ACCENT_COLOR,
                             font=('Helvetica', 12, 'bold'))

        self.style.configure('TButton',
                             background=ACCENT_COLOR,
                             foreground=FG_COLOR,
                             font=('Helvetica', 11, 'bold'),
                             padding=(6, 3))
        self.style.map('TButton',
                       background=[('active', BTN_HOVER_COLOR), ('!active', ACCENT_COLOR)],
                       foreground=[('active', FG_COLOR), ('!active', FG_COLOR)])

        self.style.configure('Vertical.TScrollbar', background=BG_COLOR, troughcolor=ACCENT_COLOR,
                             arrowcolor=FG_COLOR, bordercolor=ACCENT_COLOR, lightcolor=ACCENT_COLOR, darkcolor=ACCENT_COLOR)

    def create_widgets(self):
        # Cofres
        frame_cofre = ttk.LabelFrame(self, text="Cofres")
        frame_cofre.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_cofre, text="Selecione Cofre:").pack(side="left", padx=5)
        self.combo_cofres = ttk.Combobox(frame_cofre, state="readonly", width=40)
        self.combo_cofres.pack(side="left", padx=5, pady=5)
        self.combo_cofres.bind("<<ComboboxSelected>>", self.on_cofre_selecionado)

        ttk.Button(frame_cofre, text="Criar Cofre", command=self.criar_cofre).pack(side="left", padx=8, pady=4)

        # Pastas
        frame_pasta = ttk.LabelFrame(self, text="Pastas")
        frame_pasta.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_pasta, text="Selecione Pasta:").pack(side="left", padx=5)
        self.combo_pastas = ttk.Combobox(frame_pasta, state="readonly", width=40)
        self.combo_pastas.pack(side="left", padx=5, pady=5)
        self.combo_pastas.bind("<<ComboboxSelected>>", self.on_pasta_selecionada)

        ttk.Button(frame_pasta, text="Criar Pasta", command=self.criar_pasta).pack(side="left", padx=8, pady=4)

        # Documentos
        frame_docs = ttk.LabelFrame(self, text="Documentos")
        frame_docs.pack(fill="x", padx=15, pady=10)

        ttk.Button(frame_docs, text="Listar Documentos", command=self.listar_documentos).pack(side="left", padx=8, pady=4)
        ttk.Button(frame_docs, text="Upload Documento", command=self.upload_documento).pack(side="left", padx=8, pady=4)

        # Output / Logs
        frame_out = ttk.LabelFrame(self, text="Saída / Logs")
        frame_out.pack(fill="both", expand=True, padx=15, pady=15)

        frame_text_scroll = ttk.Frame(frame_out)
        frame_text_scroll.pack(fill="both", expand=True)

        self.text_out = tk.Text(frame_text_scroll, state="disabled", wrap="word",
                                bg=BG_COLOR, fg=FG_COLOR,
                                insertbackground=FG_COLOR,
                                font=('Consolas', 11), relief='flat')
        self.text_out.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_text_scroll, orient="vertical", command=self.text_out.yview, style='Vertical.TScrollbar')
        scrollbar.pack(side="right", fill="y")

        self.text_out.config(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="Limpar Log", command=self.limpar_log).pack(pady=(0,15))

    def log(self, msg):
        self.text_out.config(state="normal")
        self.text_out.insert("end", msg + "\n")
        self.text_out.see("end")
        self.text_out.config(state="disabled")

    def limpar_log(self):
        self.text_out.config(state="normal")
        self.text_out.delete("1.0", "end")
        self.text_out.config(state="disabled")

    def atualizar_cofres(self):
        self.assinador.listar_cofres()
        cofres = list(self.assinador.cofres.keys())
        self.combo_cofres['values'] = cofres
        if cofres:
            self.combo_cofres.current(0)
            self.on_cofre_selecionado()

    def on_cofre_selecionado(self, event=None):
        cofre = self.combo_cofres.get()
        if cofre:
            self.assinador.cofre_selecionado = cofre
            self.assinador.uuid_cofre = self.assinador.cofres[cofre]
            self.log(f"Cofre selecionado: {cofre}")
            self.atualizar_pastas()

    def atualizar_pastas(self):
        cofre = self.assinador.cofre_selecionado
        if not cofre:
            self.combo_pastas['values'] = []
            return

        pastas = self.assinador.listar_pastas(cofre)
        nomes = [p['name'] for p in pastas] if pastas else []
        self.combo_pastas['values'] = nomes
        if nomes:
            self.combo_pastas.current(0)
            self.on_pasta_selecionada()
        else:
            self.combo_pastas.set('')
            self.assinador.pasta_selecionada = None
            self.assinador.uuid_pasta = None

    def on_pasta_selecionada(self, event=None):
        nome_pasta = self.combo_pastas.get()
        if not nome_pasta:
            return
        pastas = self.assinador.listar_pastas(self.assinador.cofre_selecionado)
        for p in pastas:
            if p['name'] == nome_pasta:
                self.assinador.pasta_selecionada = nome_pasta
                self.assinador.uuid_pasta = p['uuid_folder']
                self.log(f"Pasta selecionada: {nome_pasta}")
                return

    def criar_cofre(self):
        nome = simpledialog.askstring("Criar Cofre", "Nome do novo cofre:")
        if nome:
            try:
                self.assinador.criar_cofre(nome)
                self.log(f"Cofre '{nome}' criado.")
                self.atualizar_cofres()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao criar cofre: {e}")

    def criar_pasta(self):
        nome = simpledialog.askstring("Criar Pasta", "Nome da nova pasta:")
        if nome:
            if not self.assinador.uuid_cofre:
                messagebox.showerror("Erro", "Selecione um cofre antes de criar uma pasta.")
                return
            try:
                self.assinador.criar_pastas(nome)
                self.log(f"Pasta '{nome}' criada.")
                self.atualizar_pastas()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao criar pasta: {e}")

    def listar_documentos(self):
        if not self.assinador.uuid_cofre or not self.assinador.uuid_pasta:
            messagebox.showerror("Erro", "Selecione um cofre e uma pasta primeiro.")
            return

        url = f"{self.assinador.base_url}/documents"
        params = {
            "tokenAPI": self.assinador.token,
            "cryptKey": self.assinador.cryptKey,
            "uuid_safe": self.assinador.uuid_cofre,
            "folder": self.assinador.uuid_pasta
        }

        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                documentos = response.json()
                if not documentos:
                    self.log("Nenhum documento encontrado nesta pasta.")
                    return
                self.log("Documentos encontrados:")
                for doc in documentos:
                    nome = doc.get("name", "[Sem nome]")
                    uuid = doc.get("uuid", "[Sem UUID]")
                    data = doc.get("created", "[Sem data]")
                    self.log(f" - {nome} | UUID: {uuid} | Criado em: {data}")
            else:
                self.log(f"Erro ao listar documentos: {response.status_code} - {response.text}")
        except Exception as e:
            self.log(f"Erro ao conectar ao servidor: {e}")

    def upload_documento(self):
        if not self.assinador.uuid_cofre or not self.assinador.uuid_pasta:
            messagebox.showerror("Erro", "Selecione um cofre e uma pasta antes do upload.")
            return

        path = filedialog.askopenfilename(title="Selecione o arquivo para upload", filetypes=[("PDF Files", "*.pdf")])
        if not path:
            return

        try:
            self.assinador.upload_documento(path)
            self.log("Upload realizado com sucesso!")
        except Exception as e:
            self.log(f"Erro no upload: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
