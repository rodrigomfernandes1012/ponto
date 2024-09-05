from flask import Flask, request, jsonify,  render_template, url_for, request, redirect, flash
from flask_cors import CORS
import os
from datetime import datetime
from pytz import timezone
import json
import string
import random
import requests
from dotenv import load_dotenv


load_dotenv()
api_key: str = os.getenv("api_key")

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

Origem = "Rua da Conceição 188"
Destino = ""
Valor = "0"



def random_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def data():
    data_e_hora_atuais = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    Data = data_e_hora_sao_paulo.strftime('%d/%m/%Y %H:%M')
    return Data

def hora():
    data_e_hora_atuais = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    Hora = data_e_hora_sao_paulo.strftime('%H:%M:%S')
    return Hora


def gerachamado(codigo, name, phone, pagamento, Origem):
    Data = str(data())

    Hora = str(hora())
    booking_hash = random_generator()
    url = "https://portal.taxidigital.net/APITD/api/booking/add/json"

    payload = json.dumps({
        "user_email": "",
        "user_phone": phone,
        "user_name": name,
        "init_address_name": Origem,
        "init_address_lat": -22.8948949,
        "init_address_lng": -43.1185468,
        "init_address_number": "",
        "init_reference": "",
        "init_cep": "",
        "init_real_lat": -22.8948949,
        "init_real_lng": -43.1185468,
        "end_address_name": Destino,
        "end_address_lat": -22.8948949,
        "end_address_lng": -43.11833,
        "payment_id": pagamento,
        "preferences": "",
        "schedule": 1,
        "schedule_time": Hora,
        "schedule_lead_time": "0",
        "external_authorization_id": "",
        "estimate_fare": Valor,
        "estimate_km": "",
        "user_imei": "",
        "driver_observation": "",
        "operator_observation": codigo,
        "user_platform": "1",
        "category_id": "",
        "unique_field": "",
        "share_group": "",
        "contract_number": "101275",
        "estimate_id": "",
        "booking_hash": booking_hash,
        "schedule_date": Data,
        "unique_fields": []
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload)


@app.route('/<codigo>')
def index(codigo):
    if codigo == "101275":
        image_url = "static/lig.jpeg"
    if codigo == "101276":
        image_url = "static/tx20.jpeg"
    #print(codigo)
    return render_template("index.html", codigo=codigo, image_url=image_url)

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    codigo = data.get('codigo')
    payment_method = data.get('payment_method')

    data_dict = {
        "name": name,
        "phone": phone,
        "codigo": codigo,
        "payment_method": payment_method
    }

    # Aqui você pode processar ou armazenar o dicionário como necessário
    print(data_dict)
    gerachamado(codigo, name, phone, payment_method, Origem)
    return jsonify({"message": "Obrigado por solicitar o Táxi", "data": data_dict})
@app.route('/dados', methods=['POST'])
def receber_dados():
    try:
        # Receber o JSON da requisição
        data = request.get_json()

        # Separar os dados em variáveis
        nome = data.get('nome')
        endereco_partida = data.get('endereco_partida')
        endereco_destino = data.get('endereco_destino')
        data_horario = data.get('data_horario')
        uso = data.get('uso')
        nome_empresa = data.get('nome_empresa')
        para_outra_pessoa = data.get('para_outra_pessoa')
        numero_passageiros = data.get('numero_passageiros')
        recibo = data.get('recibo')
        telefone = data.get('telefone')
        preferencias_especiais = data.get('preferencias_especiais')

        gerachamado("101275", nome, telefone, 1, endereco_partida)
        print(data)
        # Retornar as variáveis como confirmação
        return jsonify({
            "nome": nome,
            "endereco_partida": endereco_partida,
            "endereco_destino": endereco_destino,
            "data_horario": data_horario,
            "uso": uso,
            "nome_empresa": nome_empresa,
            "para_outra_pessoa": para_outra_pessoa,
            "numero_passageiros": numero_passageiros,
            "recibo": recibo,
            "telefone": telefone,
            "preferencias_especiais": preferencias_especiais
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400








def main():
    port = int(os.environ.get("PORT", 80))
    app.run(host="192.168.15.200", port=port)


if __name__ == "__main__":
    main()


