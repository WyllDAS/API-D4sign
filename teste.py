
import requests

url = "https://secure.d4sign.com.br/api/v1/documents/7f54dd65-df1e-4877-9e0a-2f5a6fa31a3d/upload?tokenAPI=live_4b0975fe2f8fa2ecd93228b429a0f784ce412c3fbf425661768bcccc6991f76f&cryptKey=live_crypt_NTjzsJU2ouHFbNzgkL9QnlSwqcBcQwhJ"

payload = {
    "uuid_folder": "a13fb15d-727f-472c-8580-2b4f4f28e7a2",
    "file": "teste copy.pdf",}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)