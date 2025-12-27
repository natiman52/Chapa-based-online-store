import requests
import dotenv
import os

dotenv.load_dotenv()
      

def InitiatePayment(txt,ammount,user):
    url = "https://api.chapa.co/v1/transaction/initialize"
    headers = {
    'Authorization': f"Bearer {os.getenv('secretkey')}",
    'Content-Type': 'application/json'
    }
    payload = {
    "amount": str(ammount),
    "currency": "ETB",
    "tx_ref": txt,
    "phone_number":user.phone.as_national.replace(" ",""),
    "email":user.email,
    "callback_url":"https://188.245.105.225",
    }    
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    chekout = response.json()
    return chekout


def Verify(txt):
    url = f"https://api.chapa.co/v1/transaction/verify/{txt}"
    payload = ''
    headers = {
        'Authorization': f'Bearer {os.getenv('secretkey')}'
    }
    response = requests.get(url, headers=headers, data=payload)
    data = response.json()
    return data