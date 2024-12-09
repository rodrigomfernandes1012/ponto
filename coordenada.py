import requests
from xml.etree import ElementTree as ET

def transform_xml_bytes_to_dict(xml_bytes):
    # Decodificar os bytes para uma string
    xml_string = xml_bytes.decode('utf-8').replace('<?xml version="1.0" encoding="utf-8"?>', '')
    xml_string = xml_string.replace('<string xmlns="http://tempuri.org/">', '').replace('</string>', '').strip()
    xml_string = xml_string.replace('&lt;', '<').replace('&gt;', '>')


    xml_string = xml_string.strip()


    # Parseando o XML
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        print(f"Erro ao analisar XML: {e}")
        return None  # Retorna None em caso de erro

    data_dict = {}

    # Extraindo nrLatitude e nrLongitude
    data_dict['nrLatitude'] = root.find('nrLatitude').text if root.find('nrLatitude') is not None else print("nao ta")
    data_dict['nrLongitude'] = root.find('nrLongitude').text #if root.find('nrLongitude') is not None else None

    resultado = data_dict
    return resultado



def consulta_get_details(cd_referencia, pais='BR', filial='107', google='0', tipo_origem='2'):
    url = "https://repositorio.taxidigital.net/WsTaxidigital/WsRepositorio.asmx/GetGPD"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }

    # Montando o corpo da requisição XML
    dsXML = f"""<data>
        <cdReferencia>{cd_referencia}</cdReferencia>
        <opt>getDetails</opt>
        <cdPais>{pais}</cdPais>
        <cdFilial>{filial}</cdFilial>
        <stGoogle>{google}</stGoogle>
        <cdTipoOrigem>{tipo_origem}</cdTipoOrigem>
    </data>"""

    # Fazendo a requisição
    response = requests.post(url, data={'dsXML': dsXML}, headers=headers)
    #print(response.text)

    # Verificando se a requisição foi bem sucedida
    if response.status_code == 200:
        # Parseando a resposta XML
        return (response.content)
    else:
        return f"Erro na requisição: {response.status_code} - {response.text}"


# Exemplo de uso
cd_referencia = 'cdLocSP_ChIJ5_HkyPBgzpQRrkUPsxsvC50'
resultado = consulta_get_details(cd_referencia)

result_dict = transform_xml_bytes_to_dict(resultado)
print(result_dict)
