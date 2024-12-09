import requests
from xml.etree import ElementTree as ET



def transform_response_to_dict(xml_response, origem):
    # Converter de bytes para string e remover o prefixo e o namespace
    xml_string = xml_response.decode('utf-8').replace('<?xml version="1.0" encoding="utf-8"?>', '')
    xml_string = xml_string.replace('<string xmlns="http://tempuri.org/">', '').replace('</string>', '').strip()
    xml_string = xml_string.replace('&lt;', '<').replace('&gt;', '>')  # Decodifica as entidades XML
    print("print da string")
    print(xml_string)

    # Parseando o XML
    try:
        root = ET.fromstring(xml_string)
        #print(xml_string)
    except ET.ParseError as e:
        print(f"Erro ao analisar XML: {e}")
        return None

    # Criar uma lista para armazenar as entradas
    resultados = []

    # Iterar sobre cada <row>
    for row in root.iter('row'):

        entry = {
            "cdReferencia": row.find('cdReferencia').text,
            "dsPlace": row.find('dsPlace').text
        }

        resultados.append(entry)

    return resultados



def consulta_get_places(latitude, longitude, raio, termo, pais, filial, tipo_origem):
    url = "https://repositorio.taxidigital.net/WsTaxidigital/WsRepositorio.asmx/GetGPD"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }

    # Montando o corpo da requisição XML
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
        <dsEnderecoCompleto></dsEnderecoCompleto>
    </data>"""
    print(dsXML)
    # Fazendo a requisição
    response = requests.post(url, data={'dsXML': dsXML}, headers=headers)

    # Verificando se a requisição foi bem sucedida
    if response.status_code == 200:
        # Parseando a resposta XML
        return transform_response_to_dict(response.content, 0)
    else:
        return f"Erro na requisição: {response.status_code} - {response.text}"


# Parametrizando a consulta com variáveis
Vlatitude = '-23.54232154313991'
Vlongitude = '-46.611177535575216'
Vraio = '1000000000'
Vtermo = 'Av. São Francisco, 678 - Santa Genoveva, Goiânia - GO, 74672-010,  Brasil'
Vpais = 'BR'
Vfilial = '107'
Vtipo_origem = '2'

# Chamada da função de consulta
resultado = consulta_get_places(Vlatitude, Vlongitude, Vraio, Vtermo, Vpais, Vfilial, Vtipo_origem)
#print(resultado)

for ref in resultado:
    print('Referencia:', ref['cdReferencia'], 'Endereço:', ref['dsPlace'])

    #coordenadas = consulta_get_details(ref['cdReferencia'])
    #print(coordenadas)




