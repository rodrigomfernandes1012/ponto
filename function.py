import cv2
import io
import json
import os
import random
import requests
import string
import tempfile
import time
from datetime import datetime
from dotenv import load_dotenv
from environs import Env
from functools import wraps
from google.cloud import vision
from PIL import Image
from PIL import ImageGrab
import pytesseract
from xml.etree import ElementTree as ET
from function_ponto import Inserir_TbLog

#latitude = '-16.64'
#longitude = '-49.31'
raio = '10000000'

vresultado_origem = {'dados_viagem': []}
vresultado_destino = {'dados_viagem': []}
vresultado_dados_geral = {'dados_geral': []}



# Cria uma instância do Env
env = Env()
# Carrega as variáveis do arquivo .env
env.read_env()

# Acessa a chave da API
#API_KEY = env("API_KEY")
#GOOGLE_APPLICATION_CREDENTIALS = "credentials.json"

# Exemplo de como usar a API key
#print(f"A chave da API é: {API_KEY}")


def get_uf(endereco):
    # Dicionário com estados e suas coordenadas (latitude, longitude)
    estados = {
        'AC': [-8.77, -70.55],
        'AL': [-9.71, -35.73],
        'AM': [-3.07, -61.66],
        'AP': [1.41, -51.77],
        'BA': [-12.96, -38.51],
        'CE': [-3.71, -38.54],
        'DF': [-15.83, -47.86],
        'ES': [-19.19, -40.34],
        'GO': [-16.64, -49.31],
        'MA': [-2.55, -44.30],
        'MT': [-12.64, -55.42],
        'MS': [-20.51, -54.54],
        'MG': [-18.10, -44.38],
        'PA': [-5.53, -52.29],
        'PB': [-7.06, -35.55],
        'PR': [-24.89, -51.55],
        'PE': [-8.28, -35.07],
        'PI': [-8.28, -43.68],
        'RJ': [-22.84, -43.15],
        'RN': [-5.22, -36.52],
        'RO': [-11.22, -62.80],
        'RS': [-30.01, -51.22],
        'RR': [1.89, -61.22],
        'SC': [-27.33, -49.44],
        'SE': [-10.90, -37.07],
        'SP': [-23.55, -46.64],
        'TO': [-10.25, -48.25],
    }

    # Separar o endereço usando a vírgula
    partes = [parte.strip() for parte in endereco.split(',')]

    # Percorrer as partes do endereço em busca dos estados
    for parte in partes:
        # Verifica se a parte contém um hífen
        if '-' in parte:
            # Separa a parte em substrings por hífen
            subpartes = [subparte.strip() for subparte in parte.split('-')]
            # A última subparte pode conter a sigla do estado
            for subparte in subpartes:
                # Verifica se a subparte é uma sigla de estado
                if subparte in estados:
                    return estados[subparte]  # Retorna as coordenadas do estado se encontrado

    # Verificar as partes normais, caso o estado não estivesse entre hífen e vírgula
    for parte in partes:
        if parte in estados:
            return estados[parte]  # Retorna as coordenadas do estado se encontrado

    return "Estado não encontrado"







#from main import medir_tempo_execucao
def capture_area(top_left, bottom_right):
    # Define bbox com as coordenadas passadas como argumento
    bbox = (top_left.x, top_left.y, bottom_right.x, bottom_right.y)  # (left, upper, right, lower)
    print(f"Coordenadas da área: {bbox}")

    # Captura a imagem
    imagem = ImageGrab.grab(bbox=bbox)

    # Salva a imagem
    image_path = 'imagens/area_capturada.jpeg'
    imagem.save(image_path)

    print(f"Imagem salva em: {image_path}")


def ocr():
    imagem = cv2.imread("imagens/voucher.png")
    caminho = r"C:\Program Files\Tesseract-OCR"
    pytesseract.pytesseract.tesseract_cmd = caminho + r'\tesseract.exe'
    texto = pytesseract.image_to_string(imagem, lang="por")
    print(texto)
    print("texto ocr acima")
    texto = texto.replace('\n', ' ')
    separar_campo(texto)
    return texto

def medir_tempo_execucao(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Marca o tempo de início
        inicio = time.time()

        # Chama a função original
        resultado = func(*args, **kwargs)

        # Marca o tempo de término
        fim = time.time()

        # Calcula o tempo de execução
        duracao = fim - inicio

        print(f"A função '{func.__name__}' levou {duracao:.6f} segundos para ser executada.")

        # Retorna o resultado da função
        return resultado

    return wrapper




def transform_response_to_dict(xml_response):
    xml_string = xml_response.decode('utf-8').replace('<?xml version="1.0" encoding="utf-8"?>', '')
    xml_string = xml_string.replace('<string xmlns="http://tempuri.org/">', '').replace('</string>', '').strip()
    xml_string = xml_string.replace('&lt;', '<').replace('&gt;', '>')

    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError:
        return None

    resultados = [{
        "cdReferencia": row.find('cdReferencia').text,
        "dsPlace": row.find('dsPlace').text
    } for row in root.iter('row')]
    print("resultados transformados")
    print(resultados)
    return resultados

@medir_tempo_execucao
def consulta_get_places(latitude, longitude, raio, termo, pais='BR', filial='107', tipo_origem='2'):
    url = "https://repositorio.taxidigital.net/WsTaxidigital/WsRepositorio.asmx/GetGPD"
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

    dsXML = f"""<data>
        <opt>getPlaces</opt>
        <nrLatitude>{latitude}</nrLatitude>
        <nrLongitude>{longitude}</nrLongitude>
        <nrRaio>{raio}</nrRaio>
        <dsTermo><![CDATA[{termo}]]></dsTermo>
        <cdPais>{pais}</cdPais>
        <cdFilial>{filial}</cdFilial>
        <stGoogle>0</stGoogle>
        <cdTipoOrigem>{tipo_origem}</cdTipoOrigem>
    </data>"""

    response = requests.post(url, data={'dsXML': dsXML}, headers=headers)
    print("resultado vazio")
    print(dsXML)
    if response.status_code == 200:
        print(response.content)
        return transform_response_to_dict(response.content)
    return None

@medir_tempo_execucao
def consulta_get_details(cd_referencia, pais='BR', filial='107', google='0', tipo_origem='2'):
    url = "https://repositorio.taxidigital.net/WsTaxidigital/WsRepositorio.asmx/GetGPD"
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

    dsXML = f"""<data>
        <cdReferencia>{cd_referencia}</cdReferencia>
        <opt>getDetails</opt>
        <cdPais>{pais}</cdPais>
        <cdFilial>{filial}</cdFilial>
        <stGoogle>{google}</stGoogle>
        <cdTipoOrigem>{tipo_origem}</cdTipoOrigem>
    </data>"""
    #print(dsXML)
    response = requests.post(url, data={'dsXML': dsXML}, headers=headers)
    #print(response.text)
    if response.status_code == 200:
        return transform_xml_bytes_to_dict(response.content)
    return None

@medir_tempo_execucao
def transform_xml_bytes_to_dict(xml_bytes):

    xml_string = xml_bytes.decode('utf-8').replace('<?xml version="1.0" encoding="utf-8"?>', '')
    xml_string = xml_string.replace('<string xmlns="http://tempuri.org/">', '').replace('</string>', '').strip()
    xml_string = xml_string.replace('&lt;', '<').replace('&gt;', '>')

    try:
        root = ET.fromstring(xml_string)
        #print(root.find('nrLatitude').text)
    except ET.ParseError:
        return None  # Retorna None em caso de erro

    return {
        'nrLatitude': root.find('nrLatitude').text if root.find('nrLatitude') is not None else None,
        'nrLongitude': root.find('nrLongitude').text if root.find('nrLongitude') is not None else None
    }


def converter_data(data_string):
    # Dicionário para mapear os dias da semana
    dias_da_semana = {
        "dom.": "domingo",
        "seg.": "segunda-feira",
        "ter.": "terça-feira",
        "qua.": "quarta-feira",
        "qui.": "quinta-feira",
        "sex.": "sexta-feira",
        "sab.": "sábado"
    }
    # Remove dia da semana e substitui por vazio
    for dia_abreviado in dias_da_semana.keys():
        if dia_abreviado in data_string:
            data_string = data_string.replace(dia_abreviado, "")
            break  # Remove apenas o primeiro que encontrar
    # Remove a palavra "de" e a pontuação
    data_string = data_string.replace("de", "").replace(".", "").replace("  ", " ")
    data_string = data_string.strip()
    try:
        # Converte a string em um objeto datetime
        data_formatada = datetime.strptime(data_string, "%d %b %Y")
        # Retorna a data formatada no formato dd/mm/aaaa
        print(data_formatada.strftime("%d/%m/%Y"))
        return data_formatada.strftime("%d/%m/%Y")
    except ValueError:
        return "Formato de data inválido"


def verificar_remover_prefixo(string):
    # Verifica se a string começa com "55" e se possui mais de 11 caracteres
    if string.startswith("55") and len(string) > 11:
        return string[2:]  # Remove os dois primeiros caracteres
    return string



@medir_tempo_execucao
def separar_campo(texto):


    # Divide o texto em partes usando ":" como delimitador
    lista = texto.split(":")
    qtde_lista = len(lista)
    # Inicializa um dicionário para armazenar os dados
    dados = {
        "Voucher": None,
        "Empresa": None,
        "Viajantes": None,
        "Telefone": None,
        "Data": None,
        "Hora": None,
        "Valor": None,
        "Origem": None,
        "Destino": None,
        "Observacoes": None,
        "Latitude_Origem": '0',
        "Longitude_Origem": '0',
        "Latitude_Destino": '0',
        "Longitude_Destino": '0'
    }

    dados["Voucher"] = (lista[0])
    dados["Empresa"] = (lista[1] )
    dados["Viajantes"] = (lista[2] )
    dados["Telefone"] = (lista[3] )
    dados["Data"] = (lista[4] )
    dados["Hora"] = (lista[5] + ":" + lista[6])
    dados["Valor"] = (lista[7])
    dados["Origem"] = (lista[8])
    latitudeUF, longitudeUF = get_uf(lista[8])
    print(latitudeUF)
    print(longitudeUF)
    print("dados origem")

    print(lista[8])
    dados["Destino"] = (lista[9])
    if qtde_lista > 10:
        dados["Observacoes"] = (lista[10])
    else:
        dados["Observacoes"] = "sem obs"
    if qtde_lista > 11:
        dados["Motorista"] = (lista[11])
    else:
        dados["Motorista"] = "sem motorista"

    voucher = (dados["Voucher"]).replace("« Agendamento &", "").replace("DETALHES DA SOLICITAÇÃO", "").replace("DETALHES DO MOTORISTA", "").replace("Empresa", "").replace("« Agendamento", "").replace("DETALI DO MOTORISTA", "").replace("Agendamento #","").replace("DETALI DO MOTORISTA  resa", "").replace("resa", "").strip()
    empresa = (dados["Empresa"]).replace(" Buscar motorista  Viajantes", "").replace("Q,", "").replace("Buscar motorista Viajantes", "").strip()
    viajante = (dados["Viajantes"]).replace(" Busque pelo placa para encont  Telefone", "").replace(" Telefone", "").replace("ra encont  Telefone", "").replace("que pelo nome ou plac  ra encontrar seu mo  Telefone", "").replace("Busque pelo nome ou placa para encontrar seu mo Telefone", "").strip()
    telefone = verificar_remover_prefixo((dados["Telefone"]).replace(" Data", "").replace("+", "").strip())
    data = (dados["Data"]).replace(" Horário", "").replace(",,", ".").replace(".,", ".").replace(",.", ".").strip()
    data = converter_data(data)
    hora = (dados["Hora"]).replace(" Valor previsto", "").strip()
    valor = (dados["Valor"]).replace("R$ ", "").replace(",", ".").replace(" Origem", "").strip()
    origem = (dados["Origem"]).replace(" Destino", "").strip()
    destino = (dados["Destino"]).replace(" Observação", "").replace("totorista", "").strip()
    observacao = (dados["Observacoes"]).replace(" Motorista", "").strip()
    motoristas = (dados["Motorista"]).strip()
    coordenadas_origem = "0"
    coordenadas_destino = "0"

    dados_viagem =( 'Voucher: ' + voucher + '\n Empresa: '+ empresa + '\n Viajante: ' + viajante + ' Tel: ' + telefone + '\n Data: ' + data + ' Hora: ' + hora, ' Valor: '+ valor + '\n Origem: ' + origem + '\n Destino: ' + destino + '\n Observacao: ' + observacao)
    dados_viagem2 ={ 'voucher':  voucher,  'empresa': empresa,  'viajantes':  viajante, 'telefone': telefone,  'datas':  data,  'hora':  hora, 'valor': valor,  'origem': origem, 'destino': destino, 'observacao': observacao}
    vresultado_dados_geral['dados_geral'].clear()
    vresultado_dados_geral['dados_geral'].append(dados_viagem2)


    coordenada_origem = (consulta_get_places(latitudeUF, longitudeUF, raio, origem))

    coordenada_destino = (consulta_get_places(latitudeUF, longitudeUF, raio, destino))



    for n in coordenada_destino:

        detalhes = consulta_get_details(n['cdReferencia'])  # Chama a função para obter detalhes

        if detalhes:

            resultado = {
                'cdReferencia': n['cdReferencia'],
                'Endereco': n['dsPlace'],
                'Latitude': detalhes['nrLatitude'],
                'Longitude': detalhes['nrLongitude']
            }

            vresultado_destino['dados_viagem'].append(resultado)  # Adiciona o dicionário à lista

        else:
            print(f"Não foi possível obter detalhes para {n['cdReferencia']}.")


    for n in coordenada_origem:

        detalhes = consulta_get_details(n['cdReferencia'])  # Chama a função para obter detalhes

        if detalhes:

            resultado = {
                'cdReferencia': n['cdReferencia'],
                'Endereco': n['dsPlace'],
                'Latitude': detalhes['nrLatitude'],
                'Longitude': detalhes['nrLongitude']
            }

            vresultado_origem['dados_viagem'].append(resultado)  # Adiciona o dicionário à lista
            print(vresultado_origem)


        else:
            print(f"Não foi possível obter detalhes para {n['cdReferencia']}.")
    print("dados_viagem")
    print(dados_viagem)
    return  dados_viagem





def random_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
booking_hash = (random_generator())



def gerachamado(voucher, observacao, viajantes, telefone, origem, destino, valor, hora, data, inputLatOrigem, inputLongOrigem, inputLatDestino, inputLongDestino):

    url = "https://portal.taxidigital.net/APITD/api/booking/add/json"
    payload = json.dumps({
      "user_email": "",
      "user_phone": telefone,
      "user_name": viajantes,
      "requester_name": viajantes,
      "init_address_name": origem,
      "init_address_lat": inputLatOrigem,
      "init_address_lng":inputLongOrigem,
      "init_address_number": "",
      "init_reference": "",
      "init_cep": "",
      "init_real_lat": inputLatOrigem,
      "init_real_lng": inputLongOrigem,
      "end_address_name": destino,
      "end_address_lat": inputLatDestino,
      "end_address_lng": inputLongDestino,
      "payment_id": 2,
      "preferences": "",
      "schedule": 1,
      "schedule_time": hora,
      "schedule_lead_time": "0",
      "external_authorization_id": "75d024b7-91dc-4582-ba5a-ab4c916ee953",
      "estimate_fare": valor,
      "estimate_km": "",
      "user_imei": "",
      "driver_observation": observacao,
      "operator_observation": voucher,
      "user_platform": "1",
      "category_id": "5398",
      "unique_field": "1",
      "share_group": "",
      "contract_number": "55000",
      "estimate_id": "123",
      "booking_hash": booking_hash,
      "schedule_date": data,
      "unique_fields": [
        {
          "unique_field": "2642d092-20c9-4ec8-8547-0f05b15760b3",
          "classificators": [
            {
              "field": 0,
              "field_id": 0,
              "field_value": viajantes
            },
            {
              "field": 1,
              "field_id": 0,
              "field_value": "1"
            }
          ]
        }
      ]
    })
    print(payload)
    headers = {
      'Content-Type': 'application/json',
      'Authorization': API_KEY

    }
    #print(API_KEY)
    response = requests.request("POST", url, headers=headers, data=payload)
    #LIMPAR OS DADOS
    vresultado_origem['dados_viagem'].clear()
    vresultado_destino['dados_viagem'].clear()
    print(response.text)
    return response.json()
