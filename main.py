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
        

    def menu(self):
        while True:
            print("\nEscolha uma ação:")
            print("1 - Listar Cofres")
            print("2 - Listar Pastas")
            print("3 - Criar Cofre")
            print("4 - Criar Pasta")
            print("9 - Sair")

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
                print("Encerrando...")
                break
            else:
                print("Opção inválida!")

if __name__ == "__main__":
    token = 'live_06af34ccfb4af78705087108c672fcd083608e3e6ff31bdb5a01305de5600826'
    chave = 'live_crypt_7xNn4VIDjbL1Ko0rI7dqd0xBBMROHYOf'

    assinador = Assinaturas(token, chave)
    assinador.menu()