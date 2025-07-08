import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from main1 import Assinaturas
import requests

# Cores da empresa
BG_COLOR = "#121212"
FG_COLOR = "#FFFFFF"
ACCENT_COLOR = "#003366"
BTN_HOVER_COLOR = "#005599"

# SANDBOX
#TOKEN = 'live_06af34ccfb4af78705087108c672fcd083608e3e6ff31bdb5a01305de5600826'
#CRYPTKEY = 'live_crypt_7xNn4VIDjbL1Ko0rI7dqd0xBBMROHYOf'

#PRODUCAO
TOKEN = 'live_4b0975fe2f8fa2ecd93228b429a0f784ce412c3fbf425661768bcccc6991f76f'
CRYPTKEY = 'live_crypt_NTjzsJU2ouHFbNzgkL9QnlSwqcBcQwhJ'


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("D4Sign Gerenciador")
        self.configure(bg=BG_COLOR)

        self.style = ttk.Style(self)
        self.set_style()

        self.assinador = Assinaturas(TOKEN, CRYPTKEY)
        self.create_widgets()
        self.atualizar_cofres()

    def set_style(self):
        self.style.theme_use('clam')
        self.style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=('Segoe UI', 12, 'bold'))
        self.style.configure('TFrame', background=BG_COLOR)
        self.style.configure('TLabelframe', background=BG_COLOR, foreground=ACCENT_COLOR, font=('Segoe UI', 14, 'bold'))
        self.style.configure('TLabelframe.Label', background=BG_COLOR, foreground=ACCENT_COLOR, font=('Segoe UI', 15, 'bold'))
        self.style.configure('TCombobox', fieldbackground=BG_COLOR, background=BG_COLOR,
                             foreground=FG_COLOR, selectbackground=ACCENT_COLOR, selectforeground=FG_COLOR,
                             arrowcolor=ACCENT_COLOR, font=('Segoe UI', 12, 'bold'))
        self.style.configure('TButton', background=ACCENT_COLOR, foreground=FG_COLOR, font=('Segoe UI', 11, 'bold'),
                             padding=(6, 3))
        self.style.map('TButton', background=[('active', BTN_HOVER_COLOR), ('!active', ACCENT_COLOR)])
        self.style.configure('Vertical.TScrollbar', background=BG_COLOR, troughcolor=ACCENT_COLOR,
                             arrowcolor=FG_COLOR)

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
        ttk.Button(frame_docs, text="Adicionar Signatário e Enviar", command=self.adicionar_signatario_e_enviar).pack(side="left", padx=8, pady=4)
        # Output / Logs
        frame_out = ttk.LabelFrame(self, text="Saída / Logs")
        frame_out.pack(fill="both", expand=True, padx=15, pady=15)
        frame_text_scroll = ttk.Frame(frame_out)
        frame_text_scroll.pack(fill="both", expand=True)
        self.text_out = tk.Text(frame_text_scroll, state="disabled", wrap="word", bg=BG_COLOR, fg=FG_COLOR,
                                insertbackground=FG_COLOR, font=('Consolas', 11), relief='flat')
        self.text_out.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_text_scroll, orient="vertical", command=self.text_out.yview,
                                  style='Vertical.TScrollbar')
        scrollbar.pack(side="right", fill="y")
        self.text_out.config(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="Limpar Log", command=self.limpar_log).pack(pady=(0, 15))

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
        cofres_dict = self.assinador.listar_cofres()
        if not cofres_dict:
            self.log("Nenhum cofre encontrado.")
            return

        nomes = list(cofres_dict.keys())
        self.combo_cofres['values'] = nomes
        if nomes:
            self.combo_cofres.current(0)
            self.on_cofre_selecionado()

    def on_cofre_selecionado(self, event=None):
        nome_cofre = self.combo_cofres.get()
        if not nome_cofre:
            return
        self.assinador.cofre_selecionado = nome_cofre
        self.assinador.uuid_cofre = self.assinador.cofres[nome_cofre]
        self.log(f"Cofre selecionado: {nome_cofre}")
        self.atualizar_pastas()

    def atualizar_pastas(self):
        nome_cofre = self.assinador.cofre_selecionado
        if not nome_cofre:
            return
        pastas = self.assinador.listar_pastas(nome_cofre)
        if not pastas:
            self.combo_pastas['values'] = []
            self.assinador.uuid_pasta = None
            self.assinador.pasta_selecionada = None
            return

        nomes = [p["name"] for p in pastas]
        self.combo_pastas['values'] = nomes
        self.combo_pastas.current(0)
        self.on_pasta_selecionada()

    def on_pasta_selecionada(self, event=None):
        nome_pasta = self.combo_pastas.get()
        if not nome_pasta:
            self.assinador.pasta_selecionada = None
            self.assinador.uuid_pasta = None
            return

        pastas = self.assinador.listar_pastas(self.assinador.cofre_selecionado)
        for p in pastas:
            if p["name"] == nome_pasta:
                self.assinador.pasta_selecionada = nome_pasta
                self.assinador.uuid_pasta = p["uuid_folder"]
                self.log(f"Pasta selecionada: {nome_pasta}")
                break

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
        if not self.assinador.uuid_cofre:
            messagebox.showerror("Erro", "Selecione um cofre primeiro.")
            return

        url = f"{self.assinador.base_url}/documents"
        params = {
            "tokenAPI": self.assinador.token,
            "cryptKey": self.assinador.cryptKey
        }

        headers = {"accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                self.log(f"Erro ao listar documentos: {response.status_code} - {response.text}")
                return

            try:
                data = response.json()
            except Exception as e:
                self.log(f"Erro ao decodificar JSON: {e}")
                return

            documentos = data[1:] if isinstance(data, list) else []

            if not documentos:
                self.log("Nenhum documento encontrado.")
                return

            # Filtro idêntico ao main.py
            documentos_filtrados = [
                doc for doc in documentos
                if doc.get("uuidSafe") == self.assinador.uuid_cofre
            ]

            if not documentos_filtrados:
                self.log("Nenhum documento encontrado no cofre selecionado.")
                return

            cofre_nome = self.assinador.cofre_selecionado or "[Desconhecido]"

            self.log(f"\n📁 Documentos no cofre '{cofre_nome}':\n")

            for doc in documentos_filtrados:
                nome = doc.get("nameDoc", "[Sem nome]")
                uuid = doc.get("uuidDoc", "[Sem UUID]")
                status = doc.get("statusName", "[Sem status]")
                data = doc.get("created", "[Sem data]")
                self.log(f" - {nome} | UUID: {uuid} | Status: {status} | Criado em: {data}")

        except Exception as e:
            self.log(f"Erro ao conectar ao servidor: {e}")

    def upload_documento(self):
        if not self.assinador.uuid_cofre or not self.assinador.uuid_pasta:
            messagebox.showerror("Erro", "Selecione um cofre e uma pasta antes do upload.")
            return

        path = filedialog.askopenfilename(title="Selecione o arquivo PDF", filetypes=[("PDF Files", "*.pdf")])
        if not path:
            return

        try:
            self.assinador.upload_documento(path)
            self.log("Upload realizado com sucesso!")
        except Exception as e:
            self.log(f"Erro no upload: {e}")

    
    def adicionar_signatario_e_enviar(self):
        if not self.assinador.uuid_cofre:
            messagebox.showerror("Erro", "Selecione um cofre primeiro.")
            return

        uuid_doc = simpledialog.askstring("UUID do Documento", "Informe o UUID do documento:")
        if not uuid_doc:
            return

        email = simpledialog.askstring("Email do Signatário", "Informe o e-mail do signatário:")
        if not email:
            return

        nome = simpledialog.askstring("Nome do Signatário", "Informe o nome do signatário:")
        if not nome:
            return

        try:
            sucesso = self.assinador.adicionar_signatario_e_enviar(uuid_doc, email, nome)
            if sucesso:
                self.log("✅ Signatário adicionado e documento enviado com sucesso.")
            else:
                self.log("⚠️ Ocorreu um problema ao adicionar o signatário ou enviar o documento.")
        except Exception as e:
            self.log(f"Erro ao adicionar signatário e enviar: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
