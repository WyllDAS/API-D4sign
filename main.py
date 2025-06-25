import requests
import json
import os


class Assinaturas:
    def __init__(self, token_api, crypt_key):
        self.token = token_api
        self.cryptKey = crypt_key
        self.base_url = "https://sandbox.d4sign.com.br/api/v1" #sandbox
        #self.base_url = "https://sandbox.d4sign.com.br/api/v1" # produção
        self.cofres = {}
        self.uuid_cofre = None
        self.uuid_pasta = None
        self.cofre_selecionado = None
        self.pasta_selecionada = None

    def trocar_cofre(self):
        cofres = self.listar_cofres()
        if not cofres:
            print("Nenhum cofre disponível.")
            return

        nome_cofre = input("Digite o nome do cofre que deseja usar: ")
        if nome_cofre not in self.cofres:
            print("Cofre não encontrado.")
            return

        self.cofre_selecionado = nome_cofre
        self.uuid_cofre = self.cofres[nome_cofre]
        self.pasta_selecionada = None
        self.uuid_pasta = None

        print(f"Cofre selecionado: {nome_cofre}")
    def trocar_pasta(self):
        if not self.uuid_cofre:
            print("Nenhum cofre selecionado. Use a opção de trocar cofre primeiro.")
            return

        pastas = self.listar_pastas(self.cofre_selecionado)
        if not pastas:
            print("Nenhuma pasta encontrada.")
            return

        nome_pasta = input("Digite o nome da pasta que deseja usar: ")
        for pasta in pastas:
            if pasta.get("name") == nome_pasta:
                self.pasta_selecionada = nome_pasta
                self.uuid_pasta = pasta.get("uuid_folder")
                print(f"Pasta selecionada: {nome_pasta}")
                return

        print("Pasta não encontrada.")


    def inicializar_ambiente(self):
        print("Inicializando ambiente...\n")

        cofres = self.listar_cofres()
        if not cofres:
            print("Nenhum cofre encontrado. Encerrando.")
            exit()

        nome_cofre = input("\nDigite o nome do cofre que deseja usar: ")
        if nome_cofre not in self.cofres:
            print("Cofre inválido. Encerrando.")
            exit()

        self.cofre_selecionado = nome_cofre
        self.uuid_cofre = self.cofres[nome_cofre]

        pastas = self.listar_pastas(nome_cofre)
        if not pastas:
            print("Nenhuma pasta encontrada. Encerrando.")
            exit()

        nome_pasta = input("\nDigite o nome da pasta que deseja usar: ")
        for pasta in pastas:
            if pasta.get("name") == nome_pasta:
                self.pasta_selecionada = nome_pasta
                self.uuid_pasta = pasta.get("uuid_folder")
                break
        else:
            print("Pasta inválida. Encerrando.")
            exit()

        print(f"\n📁 Ambiente carregado: Cofre = {self.cofre_selecionado}, Pasta = {self.pasta_selecionada}")

    def criar_cofre(self, nome_cofre):
        url = f"{self.base_url}/batches?tokenAPI={self.token}&cryptKey={self.cryptKey}"

        payload = { "keys": [f"{nome_cofre}"] } #nome do cofre
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        print("Resposta:", response.status_code, response.text)

    def criar_pastas (self,pasta):

        url = f"{self.base_url}/folders/87eceead-4c5d-4f90-b164-01b20cbb02af/create?tokenAPI={self.token}&cryptKey={self.cryptKey}"

        payload = { "folder_name": f"{pasta}" }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        print("Resposta:", response.status_code, response.text)
        

    def listar_pastas (self,nome_cofre):
        if nome_cofre not in self.cofres:
            print("Cofre não encontrado. Liste os cofres primeiro.")
            return

        uuid_safe = self.cofres[nome_cofre]
        url = f"{self.base_url}/folders/{uuid_safe}/find?tokenAPI={self.token}&cryptKey={self.cryptKey}"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pastas = response.json()
            print(f"\nPastas no cofre '{nome_cofre}':")

            for pasta in pastas:
                nome = pasta.get("name", "[Sem nome]")
                uuid = pasta.get("uuid_folder", "[Sem UUID]")
                data = pasta.get("dt_cadastro", "[Sem data]")
                print(f" - {nome} | UUID: {uuid} | Criada em: {data}")

            return pastas
        else:
            print("Erro ao listar pastas:", response.status_code, response.text)
            return None
    def listar_cofres(self):
        url = f"{self.base_url}/safes?tokenAPI={self.token}&cryptKey={self.cryptKey}"

        headers = {"accept": "application/json"}
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.cofres = {item["name-safe"]: item["uuid_safe"] for item in data}

            print("\nCofres disponíveis:")
            for nome in self.cofres:
                print(f" - {nome}")
            return self.cofres
        else:
            print("Erro ao listar cofres:", response.status_code, response.text)
            return None

    def listar_documentos(self):
        if not self.uuid_cofre or not self.uuid_pasta:
            print("Cofre ou pasta não selecionado. Use as opções do menu para selecionar.")
            return

        url = f"{self.base_url}/documents"

        params = {
            "tokenAPI": self.token,
            "cryptKey": self.cryptKey,
            "uuid_safe": self.uuid_cofre,
            "folder": self.uuid_pasta
        }

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            documentos = response.json()
            if not documentos:
                print("Nenhum documento encontrado nesta pasta.")
                return

            print("\n Documentos encontrados:")
            for doc in documentos:
                nome = doc.get("name", "[Sem nome]")
                uuid = doc.get("uuid", "[Sem UUID]")
                data = doc.get("created", "[Sem data]")
                print(f" - {nome} | UUID: {uuid} | Criado em: {data}")
        else:
            print("Erro ao listar documentos:", response.status_code, response.text)

    def upload_documento(self):
        if not self.uuid_cofre or not self.uuid_pasta:
            print("Cofre ou pasta não selecionado. Use as opções do menu para selecionar.")
            return

        caminho = input("Informe o caminho completo do PDF: ").strip()

        if not os.path.isfile(caminho):
            print("Arquivo não encontrado. Verifique o caminho.")
            return

        url = f"{self.base_url}/documents/upload?tokenAPI={self.token}&cryptKey={self.cryptKey}"

        data = {
            "uuid_folder": self.uuid_pasta
        }

        with open(caminho, "rb") as f:
            files = {
                "file": f
            }

            response = requests.post(url, data=data, files=files)

        if response.status_code == 200:
            print("✅ Upload realizado com sucesso!")
            print("Resposta:", response.json())
        else:
            print("❌ Falha no upload:", response.status_code)
            print(response.text)

    def menu(self):
        while True:
            print("\nEscolha uma ação:")
            print("1 - Listar Cofres")
            print("2 - Listar Pastas")
            print("3 - Criar Cofre")
            print("4 - Criar Pasta")
            print("5 - Listar Documentos na Pasta")
            print("6 - Upload de Documento")  
            print("9 - Sair")
            print("10 - Trocar Cofre Ativo")
            print("11 - Trocar Pasta Ativa")

            

            escolha = input("Digite o número da opção: ")

            if escolha == '1':
                self.listar_cofres()
            elif escolha == '2':
                nomeCofre = input("Qual o nome do cofre?")
                self.listar_pastas(nomeCofre)
            elif escolha == '3':
                nome = input("Nome do cofre: ")
                self.criar_cofre(nome)
            elif escolha == '4':
                pastaNome = input("Nome da pasta: ")
                self.criar_pastas(pastaNome)
            elif escolha == '5':
                self.listar_documentos()

            elif escolha == '6':
                self.upload_documento()

            elif escolha == '10':
                self.trocar_cofre()
            elif escolha == '11':
                self.trocar_pasta()

            elif escolha == '9':
                print("Encerrando...")
                break
            else:
                print("Opção inválida!")

if __name__ == "__main__":
    token = 'live_06af34ccfb4af78705087108c672fcd083608e3e6ff31bdb5a01305de5600826'
    chave = 'live_crypt_7xNn4VIDjbL1Ko0rI7dqd0xBBMROHYOf'

    assinador = Assinaturas(token, chave)
    assinador.inicializar_ambiente()
    assinador.menu()