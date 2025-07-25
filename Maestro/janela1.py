import tkinter as tk
import os
from tkinter import ttk, messagebox, filedialog, simpledialog
from main1 import Assinaturas
import requests
import pandas as pd 
from datetime import datetime
import subprocess

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
        self.state("zoomed")
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
        #scrol 
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, background=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview, style='Vertical.TScrollbar')
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Vincula rolagem com a roda do mouse
        self.scrollable_frame.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # 🧩 Agora, todos os widgets devem ser adicionados a self.scrollable_frame
        self._add_interface_components()
        def voltar_para_propostas():
            try:
                subprocess.Popen(["python", "proposta-app1.py"], shell=True)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o gerador de propostas:\n{e}")

        # Criar um frame de linha com dois frames: vazio à esquerda e botões à direita
        linha_topo = ttk.Frame(self.scrollable_frame)
        linha_topo.pack(fill="x", pady=10)

        # Frame vazio que expande e empurra os botões para a direita
        espaco = ttk.Frame(linha_topo)
        espaco.pack(side="left", expand=True)

        # Frame com os botões
        frame_botoes_direita = ttk.Frame(linha_topo)
        frame_botoes_direita.pack(side="right", padx=10)

        # Botões
        ttk.Button(frame_botoes_direita, text="📄 Propostas", command=voltar_para_propostas).pack(side="left", padx=5)
        ttk.Button(frame_botoes_direita, text="🚪 Sair", command=self.destroy).pack(side="left", padx=5)
        

#-------------------------------------------------
        
    def _add_interface_components(self):
        frame_cofre = ttk.LabelFrame(self.scrollable_frame, text="Cofres")
        frame_cofre.pack(fill="x", padx=15, pady=10)
        ttk.Label(frame_cofre, text="Selecione Cofre:").pack(side="left", padx=5)
        self.combo_cofres = ttk.Combobox(frame_cofre, state="readonly", width=40)
        self.combo_cofres.pack(side="left", padx=5, pady=5)
        self.combo_cofres.bind("<<ComboboxSelected>>", self.on_cofre_selecionado)
        ttk.Button(frame_cofre, text="Criar Cofre", command=self.criar_cofre).pack(side="left", padx=8, pady=4)

        frame_pasta = ttk.LabelFrame(self.scrollable_frame, text="Pastas")  # ✅
        frame_pasta.pack(fill="x", padx=15, pady=10)
        ttk.Label(frame_pasta, text="Selecione Pasta:").pack(side="left", padx=5)
        self.combo_pastas = ttk.Combobox(frame_pasta, state="readonly", width=40)
        self.combo_pastas.pack(side="left", padx=5, pady=5)
        self.combo_pastas.bind("<<ComboboxSelected>>", self.on_pasta_selecionada)
        ttk.Button(frame_pasta, text="Criar Pasta", command=self.criar_pasta).pack(side="left", padx=8, pady=4)

        frame_documentos = ttk.LabelFrame(self.scrollable_frame, text="Documentos Disponíveis")  # ✅
        frame_documentos.pack(fill="x", padx=15, pady=10)
        ttk.Label(frame_documentos, text="Selecione Documento:").pack(side="left", padx=5)
        self.combo_documentos = ttk.Combobox(frame_documentos, state="readonly", width=60)
        self.combo_documentos.pack(side="left", padx=5, pady=5)
        self.combo_documentos.bind("<<ComboboxSelected>>", self.on_documento_selecionado)

        frame_docs = ttk.LabelFrame(self.scrollable_frame, text="Documentos")  # ✅
        frame_docs.pack(fill="x", padx=15, pady=10)
        ttk.Button(frame_docs, text="Listar Documentos", command=self.listar_documentos).pack(side="left", padx=8, pady=4)
        ttk.Button(frame_docs, text="Upload Documento", command=self.upload_documento).pack(side="left", padx=8, pady=4)
        ttk.Button(frame_docs, text="Adicionar Signatário e Enviar", command=self.adicionar_signatario_e_enviar).pack(side="left", padx=8, pady=4)
        ttk.Button(frame_docs, text="Processar Lote JSON", command=self.executar_lote).pack(side="left", padx=8, pady=4)

        frame_out = ttk.LabelFrame(self.scrollable_frame, text="Saída / Logs")  # ✅
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

        # ✅ Também adicione este botão dentro do scrollable_frame
        ttk.Button(self.scrollable_frame, text="Limpar Log", command=self.limpar_log).pack(pady=(0, 15))

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

    def atualizar_documentos(self):
        documentos = self.assinador.listar_documentos()
        if not documentos:
            self.combo_documentos['values'] = []
            self.assinador.documento_selecionado = None
            self.assinador.uuid_documento = None
            return

        nomes = [doc.get("nameDoc", "[Sem nome]") for doc in documentos]
        self.combo_documentos['values'] = nomes

        # Mapeia nome -> UUID
        self.documentos_por_nome = {
            doc.get("nameDoc", "[Sem nome]"): doc.get("uuidDoc", None)
            for doc in documentos
        }

        self.combo_documentos.current(0)
        self.on_documento_selecionado()

    def on_documento_selecionado(self, event=None):
        nome_doc = self.combo_documentos.get()
        if not nome_doc:
            self.assinador.documento_selecionado = None
            self.assinador.uuid_documento = None
            return

        uuid = self.documentos_por_nome.get(nome_doc)
        if uuid:
            self.assinador.documento_selecionado = nome_doc
            self.assinador.uuid_documento = uuid
            self.log(f"Documento selecionado: {nome_doc} | UUID: {uuid}")

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
        self.atualizar_documentos()

    def criar_pasta(self):
        nome = simpledialog.askstring("Criar Pasta", "Nome da nova pasta:")
        if nome:
            if not self.assinador.uuid_cofre:
                messagebox.showerror("Erro", "Selecione um cofre antes de criar uma pasta.")
                return
            try:
                self.assinador.criar_pastas(self.assinador.uuid_cofre, nome)
                self.log(f"Pasta '{nome}' criada.")
                self.atualizar_pastas()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao criar pasta: {e}")

    def criar_cofre(self):
        nome = simpledialog.askstring("Criar Cofre", "Nome do novo cofre:")
        if nome:
            try:
                self.assinador.criar_cofre(nome)
                self.log(f"Cofre '{nome}' criado.")
                self.atualizar_cofres()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao criar cofre: {e}")

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
            documentos_exportar = []

            for doc in documentos_filtrados:
                nome = doc.get("nameDoc", "[Sem nome]")
                uuid = doc.get("uuidDoc", "[Sem UUID]")
                status = doc.get("statusName", "[Sem status]")
                safe = doc.get("safeName", "[Sem cofre]")

                self.log(f" - {nome} | UUID: {uuid} | Status: {status} | Cofre: {safe}")

                documentos_exportar.append({
                    "Nome": nome,
                    "UUID": uuid,
                    "Status": status,
                    "Cofre": safe
                })

            # 🧾 Após listar, perguntar onde salvar
            if documentos_exportar:
                pasta_destino = filedialog.askdirectory(title="Selecione a pasta para salvar o Excel")

                if pasta_destino:
                    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nome_arquivo = f"documentos_d4sign_{agora}.xlsx"
                    caminho_completo = os.path.join(pasta_destino, nome_arquivo)

                    try:
                        df = pd.DataFrame(documentos_exportar)
                        df.to_excel(caminho_completo, index=False)
                        self.log(f"\n✅ Arquivo Excel salvo com sucesso:\n{caminho_completo}")
                    except Exception as e:
                        self.log(f"\n❌ Erro ao salvar Excel: {e}")
                else:
                    self.log("Operação cancelada: Nenhuma pasta foi selecionada.")

            for doc in documentos_filtrados:
                nome = doc.get("nameDoc", "[Sem nome]")
                uuid = doc.get("uuidDoc", "[Sem UUID]")
                status = doc.get("statusName", "[Sem status]")
                safe = doc.get("safeName","[Sem confre]")
                self.log(f" - {nome} | UUID: {uuid} | Status: {status} | Cofre: {safe}")

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

    def executar_lote(self):
        if not self.assinador.uuid_cofre or not self.assinador.uuid_pasta:
            messagebox.showerror("Erro", "Selecione um cofre e uma pasta primeiro.")
            return

        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo JSON",
            filetypes=[("JSON Files", "*.json")]
        )

        if not caminho:
            return

        try:
            self.assinador.processar_lote_de_assinaturas(caminho)
            self.log("✅ Lote processado.")
        except Exception as e:
            self.log(f"❌ Erro ao processar lote: {e}")


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
