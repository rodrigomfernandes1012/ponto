from flask import Flask, jsonify,  render_template, url_for, request, redirect, flash
import mysql.connector
from forms import FormLogin, FormCriarConta, FormProduto, FormCliente, FormDestinatario, FormUsuario, FuncionarioForm
import folium
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from datetime import datetime
import json


token = "8c4EF9vXi8TZe6581e0af85c25"

def conecta_bd():
  conexao = mysql.connector.connect(
  host='dbintellimetrics.c3kc6gou2fhz.us-west-2.rds.amazonaws.com',
  user='admin',
  password='IntelliMetr!c$',
  database='DbIntelliMetrics')
  return conexao




def ponto():
    url = "https://replit.taxidigital.net/Ponto"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    selecao = json.loads(response.text)
    #print(selecao)
    dados_dicionario = {}

   # for dado in selecao:
   #     datahora = (dado["dsRegistro01"])
   #     data_datetime = datetime.strptime(datahora, "%a, %d %b %Y %H:%M:%S %Z")
   #     hora_minutos = data_datetime.strftime("%H:%M")
   #     print("Hora e minutos:", hora_minutos)



  #print(selecao)
    for registro in selecao:
        #nome = registro['dsCardNo']
        #print(registro)
        nome = registro['dsCardName']
        #print(nome)
        #datacompleta = int(registro['dsUtc'])
        #data = (datetime.utcfromtimestamp(datacompleta).strftime('%Y-%m-%d %H:%M:%S'))
        #hora = (datetime.utcfromtimestamp(datacompleta).strftime('%H:%M:%S'))
        #data = (datetime.utcfromtimestamp(datacompleta).strftime('%d-%m-%Y'))
        #print(data)
        dados_dicionario[nome] = []
        dados_dicionario[nome] = [data]
        dados_dicionario[nome].append(data)

        return selecao
##        print(selecao)



def get_ponto():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbAcessoIntelBras where dsStatus = 1 and dsUtc >= 1722502193 ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  # Criar o dicionário
  dados_dicionario = {}

  #print(selecao)
  for registro in selecao:
      nome = registro['dsCardName']
      #print(nome)
      datacompleta = int(registro['dsUtc'])
      #data = (datetime.utcfromtimestamp(datacompleta).strftime('%Y-%m-%d %H:%M:%S'))
      #hora = (datetime.utcfromtimestamp(datacompleta).strftime('%H:%M:%S'))
      data = (datetime.utcfromtimestamp(datacompleta).strftime('%d-%m-%Y'))
      #print(data)
      dados_dicionario[nome] = []
      dados_dicionario[nome] = [data]

      dados_dicionario[nome].append(data)
      #dados_dicionario[hora] = []
      #dados_dicionario[hora] = [hora]
      #dados_dicionario[nome].append(hora)
      #dados_dicionario[nome] =  [data]
      #dados_dicionario[nome] = {'data': registro['dsUtc']}
  cursor.close()
  conexao.close()
  #print(dados_dicionario)
  return selecao



def getponto():
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
    comando = f'SELECT dsCardNo FROM DbIntelliMetrics.TbAcessoIntelBras where dsStatus = 1 and dsutc >=1722506000 group by dsCardNo, dsCardName order by dsCardname;'
    cursor.execute(comando)
    funcionarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    # Array para armazenar os resultados
    funcionarios_json = []




    # Percorre os funcionarios
    for funcionario in funcionarios:
        (
            dsCardNo,
        ) = funcionario

        dsCardNo = (funcionario['dsCardNo'])
        print(dsCardNo)
        funcionarios_json.append(funcionario)

        conexao = conecta_bd()
        cursor = conexao.cursor(dictionary=True)
        comando = f'SELECT dsUtc FROM DbIntelliMetrics.TbAcessoIntelBras where dsStatus = 1 and dsutc >=1722506000  and dsCardNo = {dsCardNo};'
        cursor.execute(comando)
        datas = cursor.fetchall()
        print(datas)
        cursor.close()
        conexao.close()
    #return jsonify(funcionarios_json)
#getponto()













def pesquisa_posicoes():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbPosicao ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

#posicoes = [{'cdPosicao': 28, 'dsModelo': '0ST410STT', 'dtData': '20240128', 'dtHora': '13:06:26', 'dsLat': '-21.113379', 'dsLong': '-056.480550', 'nrTemp': 34.1, 'nrBat': 3.81, 'nrSeq': 4817, 'dsArquivo': '109789367', 'cdDispositivo': 0, 'dsEndereco': None}, {'cdPosicao': 29, 'dsModelo': '0ST410STT', 'dtData': '20240128', 'dtHora': '13:06:26', 'dsLat': '-21.113379', 'dsLong': '-056.480550', 'nrTemp': 34.1, 'nrBat': 3.81, 'nrSeq': 4817, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 31, 'dsModelo': '0ST410STT', 'dtData': '20240128', 'dtHora': '13:06:26', 'dsLat': '-21.113379', 'dsLong': '-056.480550', 'nrTemp': 34.1, 'nrBat': 3.81, 'nrSeq': 4817, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 32, 'dsModelo': '0ST410STT', 'dtData': '20240128', 'dtHora': '13:06:26', 'dsLat': '-21.113379', 'dsLong': '-056.480550', 'nrTemp': 34.1, 'nrBat': 3.81, 'nrSeq': 4817, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 33, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '01:44:52', 'dsLat': '-23.502991', 'dsLong': '-046.488657', 'nrTemp': 26.9, 'nrBat': 3.77, 'nrSeq': 5486, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 34, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.522828', 'dsLong': '-046.519373', 'nrTemp': 27.9, 'nrBat': 3.76, 'nrSeq': 5503, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 35, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.522828', 'dsLong': '-046.519373', 'nrTemp': 28.1, 'nrBat': 3.76, 'nrSeq': 5502, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 36, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.522828', 'dsLong': '-046.519373', 'nrTemp': 26.5, 'nrBat': 3.76, 'nrSeq': 5499, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 37, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.522828', 'dsLong': '-046.519373', 'nrTemp': 24.6, 'nrBat': 3.76, 'nrSeq': 5498, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 38, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '12:34:21', 'dsLat': '-23.522847', 'dsLong': '-046.519405', 'nrTemp': 23.8, 'nrBat': 3.76, 'nrSeq': 5496, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 39, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '08:13:03', 'dsLat': '-23.502739', 'dsLong': '-046.488550', 'nrTemp': 23.8, 'nrBat': 3.76, 'nrSeq': 5492, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 40, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '02:46:52', 'dsLat': '-23.503013', 'dsLong': '-046.488731', 'nrTemp': 26.2, 'nrBat': 3.77, 'nrSeq': 5487, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 41, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '22:23:45', 'dsLat': '-23.502983', 'dsLong': '-046.488637', 'nrTemp': 24.6, 'nrBat': 3.76, 'nrSeq': 5505, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 42, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '21:18:21', 'dsLat': '-23.503178', 'dsLong': '-046.488812', 'nrTemp': 24.2, 'nrBat': 3.76, 'nrSeq': 5504, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 43, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '23:28:52', 'dsLat': '-23.503115', 'dsLong': '-046.488811', 'nrTemp': 25.1, 'nrBat': 3.76, 'nrSeq': 5506, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 44, 'dsModelo': 'ST410STT', 'dtData': '20240222', 'dtHora': '00:30:21', 'dsLat': '-23.503004', 'dsLong': '-046.488752', 'nrTemp': 25.0, 'nrBat': 3.76, 'nrSeq': 5507, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 45, 'dsModelo': 'ST410STT', 'dtData': '20240222', 'dtHora': '11:05:54', 'dsLat': '-23.502970', 'dsLong': '-046.488616', 'nrTemp': 22.5, 'nrBat': 3.76, 'nrSeq': 5517, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 46, 'dsModelo': 'ST410STT', 'dtData': '20240222', 'dtHora': '10:00:47', 'dsLat': '-23.503174', 'dsLong': '-046.488759', 'nrTemp': 22.6, 'nrBat': 3.76, 'nrSeq': 5516, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 47, 'dsModelo': 'ST410STT', 'dtData': '20240222', 'dtHora': '08:56:02', 'dsLat': '-23.502934', 'dsLong': '-046.488691', 'nrTemp': 22.6, 'nrBat': 3.76, 'nrSeq': 5515, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 48, 'dsModelo': 'ST410STT', 'dtData': '20240222', 'dtHora': '07:50:51', 'dsLat': '-23.502955', 'dsLong': '-046.488780', 'nrTemp': 22.9, 'nrBat': 3.76, 'nrSeq': 5514, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 49, 'dsModelo': 'ST410STT', 'dtData': '20240222', 'dtHora': '12:11:09', 'dsLat': '-23.492708', 'dsLong': '-046.474271', 'nrTemp': 29.9, 'nrBat': 3.75, 'nrSeq': 5518, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 50, 'dsModelo': 'ST410STT', 'dtData': '20240222', 'dtHora': '13:12:01', 'dsLat': '-23.502995', 'dsLong': '-046.488825', 'nrTemp': 25.4, 'nrBat': 3.76, 'nrSeq': 5519, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 51, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.502972', 'dsLong': '-046.488797', 'nrTemp': 26.0, 'nrBat': 3.76, 'nrSeq': 5520, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 52, 'dsModelo': 'ST410STT', 'dtData': '20240222', 'dtHora': '15:21:32', 'dsLat': '-23.558499', 'dsLong': '-046.660656', 'nrTemp': 29.9, 'nrBat': 3.75, 'nrSeq': 5521, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 53, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.558578', 'dsLong': '-046.660522', 'nrTemp': 28.8, 'nrBat': 3.75, 'nrSeq': 5522, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 54, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503062', 'dsLong': '-046.488730', 'nrTemp': 29.6, 'nrBat': 3.75, 'nrSeq': 5528, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 55, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503062', 'dsLong': '-046.488730', 'nrTemp': 30.5, 'nrBat': 3.75, 'nrSeq': 5527, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 56, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503062', 'dsLong': '-046.488730', 'nrTemp': 28.8, 'nrBat': 3.75, 'nrSeq': 5529, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 57, 'dsModelo': 'ST410STT', 'dtData': '20240223', 'dtHora': '01:08:21', 'dsLat': '-23.486845', 'dsLong': '-046.503987', 'nrTemp': 31.5, 'nrBat': 3.75, 'nrSeq': 5530, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 58, 'dsModelo': 'ST410STT', 'dtData': '20240223', 'dtHora': '02:13:21', 'dsLat': '-23.503053', 'dsLong': '-046.488748', 'nrTemp': 31.5, 'nrBat': 3.75, 'nrSeq': 5531, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 59, 'dsModelo': 'ST410STT', 'dtData': '20240223', 'dtHora': '03:15:52', 'dsLat': '-23.502945', 'dsLong': '-046.488650', 'nrTemp': 30.5, 'nrBat': 3.75, 'nrSeq': 5532, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 60, 'dsModelo': 'ST410STT', 'dtData': '20240223', 'dtHora': '10:47:52', 'dsLat': '-23.502946', 'dsLong': '-046.488685', 'nrTemp': 26.0, 'nrBat': 3.75, 'nrSeq': 5539, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 61, 'dsModelo': 'ST410STT', 'dtData': '20240223', 'dtHora': '09:43:02', 'dsLat': '-23.503023', 'dsLong': '-046.488832', 'nrTemp': 26.2, 'nrBat': 3.75, 'nrSeq': 5538, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 62, 'dsModelo': 'ST410STT', 'dtData': '20240223', 'dtHora': '06:28:19', 'dsLat': '-23.503044', 'dsLong': '-046.488923', 'nrTemp': 28.1, 'nrBat': 3.75, 'nrSeq': 5535, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 63, 'dsModelo': 'ST410STT', 'dtData': '20240223', 'dtHora': '11:53:16', 'dsLat': '-23.502891', 'dsLong': '-046.488680', 'nrTemp': 26.5, 'nrBat': 3.75, 'nrSeq': 5540, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 64, 'dsModelo': 'ST410STT', 'dtData': '20240223', 'dtHora': '12:56:00', 'dsLat': '-23.533441', 'dsLong': '-046.540975', 'nrTemp': 27.2, 'nrBat': 3.75, 'nrSeq': 5541, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 65, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 30.6, 'nrBat': 3.75, 'nrSeq': 5544, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 66, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 30.3, 'nrBat': 3.75, 'nrSeq': 5543, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 67, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 31.1, 'nrBat': 3.75, 'nrSeq': 5545, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 68, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 31.5, 'nrBat': 3.75, 'nrSeq': 5546, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 69, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 32.4, 'nrBat': 3.75, 'nrSeq': 5547, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 70, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 30.5, 'nrBat': 3.75, 'nrSeq': 5549, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 71, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 31.4, 'nrBat': 3.75, 'nrSeq': 5548, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 72, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.7, 'nrBat': 3.75, 'nrSeq': 5550, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 73, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.2, 'nrBat': 3.75, 'nrSeq': 5551, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 74, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.5, 'nrBat': 3.74, 'nrSeq': 5561, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 75, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.2, 'nrBat': 3.74, 'nrSeq': 5560, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 76, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.5, 'nrBat': 3.74, 'nrSeq': 5557, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 77, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.2, 'nrBat': 3.75, 'nrSeq': 5553, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 78, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.5, 'nrBat': 3.74, 'nrSeq': 5562, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 79, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.0, 'nrBat': 3.74, 'nrSeq': 5572, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 80, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.0, 'nrBat': 3.74, 'nrSeq': 5573, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 81, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.8, 'nrBat': 3.74, 'nrSeq': 5574, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 82, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.0, 'nrBat': 3.73, 'nrSeq': 5607, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 83, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.7, 'nrBat': 3.73, 'nrSeq': 5606, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 84, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.6, 'nrBat': 3.73, 'nrSeq': 5605, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 85, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.0, 'nrBat': 3.73, 'nrSeq': 5601, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 86, 'dsModelo': 'ST410STT', 'dtData': '20240226', 'dtHora': '12:57:39', 'dsLat': '-23.540123', 'dsLong': '-046.578893', 'nrTemp': 30.2, 'nrBat': 3.72, 'nrSeq': 5608, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 87, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.1, 'nrBat': 3.73, 'nrSeq': 5595, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 88, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.4, 'nrBat': 3.73, 'nrSeq': 5592, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 89, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 29.0, 'nrBat': 3.73, 'nrSeq': 5588, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 90, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.8, 'nrBat': 3.73, 'nrSeq': 5586, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 91, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.7, 'nrBat': 3.73, 'nrSeq': 5585, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 92, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.6, 'nrBat': 3.73, 'nrSeq': 5581, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 93, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503130', 'dsLong': '-046.488820', 'nrTemp': 28.7, 'nrBat': 3.73, 'nrSeq': 5580, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 94, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '01:44:52', 'dsLat': '-23.502991', 'dsLong': '-046.488657', 'nrTemp': 26.9, 'nrBat': 3.77, 'nrSeq': 5486, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 95, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '01:44:52', 'dsLat': '-23.502991', 'dsLong': '-046.488657', 'nrTemp': 26.9, 'nrBat': 3.77, 'nrSeq': 5486, 'dsArquivo': '109789367', 'cdDispositivo': 442, 'dsEndereco': None}, {'cdPosicao': 96, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '01:44:52', 'dsLat': '-23.502991', 'dsLong': '-046.488657', 'nrTemp': 26.9, 'nrBat': 3.77, 'nrSeq': 5486, 'dsArquivo': '109789367', 'cdDispositivo': 1, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 97, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '01:44:52', 'dsLat': '-23.502991', 'dsLong': '-046.488657', 'nrTemp': 26.9, 'nrBat': 3.77, 'nrSeq': 5486, 'dsArquivo': '109789367', 'cdDispositivo': 1, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 98, 'dsModelo': 'ST410STT', 'dtData': '20240221', 'dtHora': '01:44:52', 'dsLat': '-23.502991', 'dsLong': '-046.488657', 'nrTemp': 26.9, 'nrBat': 3.77, 'nrSeq': 5486, 'dsArquivo': '1-20240227163220', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 99, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 32.3, 'nrBat': 3.71, 'nrSeq': 5636, 'dsArquivo': '1-20240227171300', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 100, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 32.0, 'nrBat': 3.71, 'nrSeq': 5635, 'dsArquivo': '2-20240227171310', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 101, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 31.5, 'nrBat': 3.71, 'nrSeq': 5634, 'dsArquivo': '3-20240227171316', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 102, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 29.0, 'nrBat': 3.72, 'nrSeq': 5630, 'dsArquivo': '4-20240227171322', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 103, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 28.6, 'nrBat': 3.72, 'nrSeq': 5628, 'dsArquivo': '5-20240227171328', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 104, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 28.7, 'nrBat': 3.72, 'nrSeq': 5626, 'dsArquivo': '6-20240227171334', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 105, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 29.1, 'nrBat': 3.72, 'nrSeq': 5622, 'dsArquivo': '7-20240227171340', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 106, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 29.5, 'nrBat': 3.72, 'nrSeq': 5618, 'dsArquivo': '8-20240227171346', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 107, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 29.5, 'nrBat': 3.72, 'nrSeq': 5617, 'dsArquivo': '9-20240227171352', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 108, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540027', 'dsLong': '-046.578952', 'nrTemp': 30.3, 'nrBat': 3.73, 'nrSeq': 5614, 'dsArquivo': '10-20240227171357', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 109, 'dsModelo': 'ST410STT', 'dtData': '20240226', 'dtHora': '16:07:54', 'dsLat': '-23.539811', 'dsLong': '-046.578948', 'nrTemp': 43.9, 'nrBat': 3.72, 'nrSeq': 5611, 'dsArquivo': '11-20240227171403', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 110, 'dsModelo': 'ST410STT', 'dtData': '20240227', 'dtHora': '21:16:00', 'dsLat': '-23.503066', 'dsLong': '-046.488841', 'nrTemp': 29.0, 'nrBat': 3.72, 'nrSeq': 5638, 'dsArquivo': '12-20240227181559', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 191, São Paulo, Brazil'}, {'cdPosicao': 111, 'dsModelo': 'ST410STT', 'dtData': '20240227', 'dtHora': '22:18:01', 'dsLat': '-23.502948', 'dsLong': '-046.488661', 'nrTemp': 31.2, 'nrBat': 3.71, 'nrSeq': 5639, 'dsArquivo': '13-20240227191801', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 112, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '10:59:30', 'dsLat': '-23.502812', 'dsLong': '-046.488596', 'nrTemp': 27.9, 'nrBat': 3.71, 'nrSeq': 5651, 'dsArquivo': '1-20240228090229', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 113, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '12:04:09', 'dsLat': '-23.540262', 'dsLong': '-046.578961', 'nrTemp': 24.6, 'nrBat': 3.71, 'nrSeq': 5652, 'dsArquivo': '2-20240228090552', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 114, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '10:59:30', 'dsLat': '-23.502812', 'dsLong': '-046.488596', 'nrTemp': 27.9, 'nrBat': 3.71, 'nrSeq': 5651, 'dsArquivo': '3-20240228090558', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 115, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '07:48:53', 'dsLat': '-23.502932', 'dsLong': '-046.488712', 'nrTemp': 28.7, 'nrBat': 3.71, 'nrSeq': 5648, 'dsArquivo': '4-20240228090638', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 116, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '06:45:46', 'dsLat': '-23.502838', 'dsLong': '-046.486438', 'nrTemp': 29.4, 'nrBat': 3.71, 'nrSeq': 5647, 'dsArquivo': '5-20240228090645', 'cdDispositivo': 442, 'dsEndereco': 'Rua Roque Jose Dias 31 UNDOS, São Paulo, Brazil'}, {'cdPosicao': 117, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '12:10:09', 'dsLat': '-23.540262', 'dsLong': '-046.578961', 'nrTemp': 28.6, 'nrBat': 3.71, 'nrSeq': 5653, 'dsArquivo': '6-20240228091010', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 118, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '05:41:46', 'dsLat': '-23.502870', 'dsLong': '-046.488666', 'nrTemp': 30.0, 'nrBat': 3.71, 'nrSeq': 5646, 'dsArquivo': '7-20240228091016', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 119, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '01:28:21', 'dsLat': '-23.502941', 'dsLong': '-046.488639', 'nrTemp': 26.9, 'nrBat': 3.72, 'nrSeq': 5642, 'dsArquivo': '8-20240228091029', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 120, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '00:25:15', 'dsLat': '-23.503078', 'dsLong': '-046.488655', 'nrTemp': 32.3, 'nrBat': 3.71, 'nrSeq': 5641, 'dsArquivo': '9-20240228091035', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 121, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540320', 'dsLong': '-046.578923', 'nrTemp': 30.9, 'nrBat': 3.71, 'nrSeq': 5654, 'dsArquivo': '10-20240228101543', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 122, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540320', 'dsLong': '-046.578923', 'nrTemp': 30.8, 'nrBat': 3.71, 'nrSeq': 5655, 'dsArquivo': '11-20240228112051', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 123, 'dsModelo': 'ST410STT', 'dtData': '20240304', 'dtHora': '11:02:21', 'dsLat': '-23.502945', 'dsLong': '-046.488769', 'nrTemp': 23.2, 'nrBat': 3.67, 'nrSeq': 5765, 'dsArquivo': '1-20240304090448', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 124, 'dsModelo': 'ST410STT', 'dtData': '20240304', 'dtHora': '09:58:21', 'dsLat': '-23.502966', 'dsLong': '-046.488725', 'nrTemp': 23.3, 'nrBat': 3.67, 'nrSeq': 5764, 'dsArquivo': '2-20240304090454', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 125, 'dsModelo': 'ST410STT', 'dtData': '20240304', 'dtHora': '03:39:31', 'dsLat': '-23.503194', 'dsLong': '-046.488540', 'nrTemp': 26.9, 'nrBat': 3.67, 'nrSeq': 5758, 'dsArquivo': '3-20240304090500', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 126, 'dsModelo': 'ST410STT', 'dtData': '20240304', 'dtHora': '00:28:21', 'dsLat': '-23.503031', 'dsLong': '-046.488645', 'nrTemp': 29.5, 'nrBat': 3.67, 'nrSeq': 5755, 'dsArquivo': '4-20240304090506', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 127, 'dsModelo': 'ST410STT', 'dtData': '20240303', 'dtHora': '19:11:01', 'dsLat': '-23.502833', 'dsLong': '-046.488570', 'nrTemp': 42.6, 'nrBat': 3.66, 'nrSeq': 5750, 'dsArquivo': '5-20240304090512', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 128, 'dsModelo': 'ST410STT', 'dtData': '20240303', 'dtHora': '13:53:30', 'dsLat': '-23.502992', 'dsLong': '-046.488778', 'nrTemp': 23.7, 'nrBat': 3.68, 'nrSeq': 5745, 'dsArquivo': '6-20240304090518', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 129, 'dsModelo': 'ST410STT', 'dtData': '20240303', 'dtHora': '09:40:39', 'dsLat': '-23.502835', 'dsLong': '-046.488691', 'nrTemp': 23.3, 'nrBat': 3.68, 'nrSeq': 5741, 'dsArquivo': '7-20240304090524', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 130, 'dsModelo': 'ST410STT', 'dtData': '20240303', 'dtHora': '05:27:45', 'dsLat': '-23.502881', 'dsLong': '-046.488763', 'nrTemp': 25.5, 'nrBat': 3.68, 'nrSeq': 5737, 'dsArquivo': '8-20240304090530', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 131, 'dsModelo': 'ST410STT', 'dtData': '20240303', 'dtHora': '04:24:11', 'dsLat': '-23.503229', 'dsLong': '-046.489482', 'nrTemp': 26.3, 'nrBat': 3.68, 'nrSeq': 5736, 'dsArquivo': '9-20240304090535', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 191, São Paulo, Brazil'}, {'cdPosicao': 132, 'dsModelo': 'ST410STT', 'dtData': '20240303', 'dtHora': '01:14:21', 'dsLat': '-23.503219', 'dsLong': '-046.488887', 'nrTemp': 29.5, 'nrBat': 3.68, 'nrSeq': 5733, 'dsArquivo': '10-20240304090541', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 191, São Paulo, Brazil'}, {'cdPosicao': 133, 'dsModelo': 'ST410STT', 'dtData': '20240302', 'dtHora': '19:57:52', 'dsLat': '-23.502976', 'dsLong': '-046.488758', 'nrTemp': 41.6, 'nrBat': 3.67, 'nrSeq': 5728, 'dsArquivo': '11-20240304090547', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 134, 'dsModelo': 'ST410STT', 'dtData': '20240302', 'dtHora': '15:44:51', 'dsLat': '-23.502980', 'dsLong': '-046.488855', 'nrTemp': 33.5, 'nrBat': 3.68, 'nrSeq': 5724, 'dsArquivo': '12-20240304090553', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 191, São Paulo, Brazil'}, {'cdPosicao': 135, 'dsModelo': 'ST410STT', 'dtData': '20240302', 'dtHora': '10:28:19', 'dsLat': '-23.503035', 'dsLong': '-046.488680', 'nrTemp': 23.8, 'nrBat': 3.69, 'nrSeq': 5719, 'dsArquivo': '13-20240304090559', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 136, 'dsModelo': 'ST410STT', 'dtData': '20240302', 'dtHora': '05:11:16', 'dsLat': '-23.502946', 'dsLong': '-046.488730', 'nrTemp': 25.3, 'nrBat': 3.69, 'nrSeq': 5714, 'dsArquivo': '14-20240304090605', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 137, 'dsModelo': 'ST410STT', 'dtData': '20240301', 'dtHora': '23:53:57', 'dsLat': '-23.502631', 'dsLong': '-046.488626', 'nrTemp': 30.5, 'nrBat': 3.69, 'nrSeq': 5709, 'dsArquivo': '15-20240304090611', 'cdDispositivo': 442, 'dsEndereco': 'Rua Marcopolo 350, São Paulo, Brazil'}, {'cdPosicao': 138, 'dsModelo': 'ST410STT', 'dtData': '20240301', 'dtHora': '19:40:30', 'dsLat': '-23.502985', 'dsLong': '-046.488829', 'nrTemp': 40.1, 'nrBat': 3.69, 'nrSeq': 5705, 'dsArquivo': '16-20240304090617', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 191, São Paulo, Brazil'}, {'cdPosicao': 139, 'dsModelo': 'ST410STT', 'dtData': '20240301', 'dtHora': '16:30:39', 'dsLat': '-23.502900', 'dsLong': '-046.488658', 'nrTemp': 38.7, 'nrBat': 3.69, 'nrSeq': 5702, 'dsArquivo': '17-20240304090623', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 140, 'dsModelo': 'ST410STT', 'dtData': '20240301', 'dtHora': '11:13:22', 'dsLat': '-23.502971', 'dsLong': '-046.488746', 'nrTemp': 26.0, 'nrBat': 3.7, 'nrSeq': 5697, 'dsArquivo': '18-20240304090629', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 141, 'dsModelo': 'ST410STT', 'dtData': '20240301', 'dtHora': '06:58:46', 'dsLat': '-23.502867', 'dsLong': '-046.488758', 'nrTemp': 27.3, 'nrBat': 3.7, 'nrSeq': 5693, 'dsArquivo': '19-20240304090649', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 142, 'dsModelo': 'ST410STT', 'dtData': '20240301', 'dtHora': '05:55:08', 'dsLat': '-23.502880', 'dsLong': '-046.488704', 'nrTemp': 27.6, 'nrBat': 3.7, 'nrSeq': 5692, 'dsArquivo': '20-20240304090721', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 143, 'dsModelo': 'ST410STT', 'dtData': '20240301', 'dtHora': '04:52:02', 'dsLat': '-23.502868', 'dsLong': '-046.488396', 'nrTemp': 28.1, 'nrBat': 3.7, 'nrSeq': 5691, 'dsArquivo': '21-20240304090727', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 144, 'dsModelo': 'ST410STT', 'dtData': '20240301', 'dtHora': '02:44:09', 'dsLat': '-23.503691', 'dsLong': '-046.491347', 'nrTemp': 29.0, 'nrBat': 3.7, 'nrSeq': 5689, 'dsArquivo': '22-20240304090733', 'cdDispositivo': 442, 'dsEndereco': 'Rua Professor Jose De Souza 360, São Paulo, Brazil'}, {'cdPosicao': 145, 'dsModelo': 'ST410STT', 'dtData': '20240229', 'dtHora': '23:34:21', 'dsLat': '-23.503025', 'dsLong': '-046.488820', 'nrTemp': 30.3, 'nrBat': 3.7, 'nrSeq': 5686, 'dsArquivo': '23-20240304090739', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 191, São Paulo, Brazil'}, {'cdPosicao': 146, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.513118', 'dsLong': '-046.504340', 'nrTemp': 31.8, 'nrBat': 3.7, 'nrSeq': 5681, 'dsArquivo': '24-20240304090745', 'cdDispositivo': 442, 'dsEndereco': 'Avenida Amador Bueno Da Veiga 4780, São Paulo, Brazil'}, {'cdPosicao': 147, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.513118', 'dsLong': '-046.504340', 'nrTemp': 30.0, 'nrBat': 3.7, 'nrSeq': 5678, 'dsArquivo': '25-20240304090751', 'cdDispositivo': 442, 'dsEndereco': 'Avenida Amador Bueno Da Veiga 4780, São Paulo, Brazil'}, {'cdPosicao': 148, 'dsModelo': 'ST410STT', 'dtData': '20240229', 'dtHora': '11:46:33', 'dsLat': '-23.513294', 'dsLong': '-046.504592', 'nrTemp': 31.2, 'nrBat': 3.71, 'nrSeq': 5675, 'dsArquivo': '26-20240304090809', 'cdDispositivo': 442, 'dsEndereco': 'Avenida Amador Bueno Da Veiga 4661, São Paulo, Brazil'}, {'cdPosicao': 149, 'dsModelo': 'ST410STT', 'dtData': '20240229', 'dtHora': '10:44:01', 'dsLat': '-23.502933', 'dsLong': '-046.488614', 'nrTemp': 27.6, 'nrBat': 3.7, 'nrSeq': 5674, 'dsArquivo': '27-20240304090815', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 150, 'dsModelo': 'ST410STT', 'dtData': '20240229', 'dtHora': '08:37:09', 'dsLat': '-23.502919', 'dsLong': '-046.488671', 'nrTemp': 28.1, 'nrBat': 3.7, 'nrSeq': 5672, 'dsArquivo': '28-20240304090835', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 151, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.502995', 'dsLong': '-046.488607', 'nrTemp': 28.2, 'nrBat': 3.7, 'nrSeq': 5671, 'dsArquivo': '29-20240304090841', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 152, 'dsModelo': 'ST410STT', 'dtData': '20240229', 'dtHora': '06:27:51', 'dsLat': '-23.502992', 'dsLong': '-046.488613', 'nrTemp': 27.7, 'nrBat': 3.71, 'nrSeq': 5670, 'dsArquivo': '30-20240304090855', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 153, 'dsModelo': 'ST410STT', 'dtData': '20240229', 'dtHora': '05:25:09', 'dsLat': '-23.502776', 'dsLong': '-046.488272', 'nrTemp': 27.6, 'nrBat': 3.7, 'nrSeq': 5669, 'dsArquivo': '31-20240304090901', 'cdDispositivo': 442, 'dsEndereco': 'Avenida Boturussu 482, São Paulo, Brazil'}, {'cdPosicao': 154, 'dsModelo': 'ST410STT', 'dtData': '20240229', 'dtHora': '00:04:21', 'dsLat': '-23.492879', 'dsLong': '-046.476170', 'nrTemp': 30.0, 'nrBat': 3.71, 'nrSeq': 5664, 'dsArquivo': '32-20240304090924', 'cdDispositivo': 442, 'dsEndereco': 'Rua Miguel Rachid 196, São Paulo, Brazil'}, {'cdPosicao': 155, 'dsModelo': 'ST410STT', 'dtData': '20240228', 'dtHora': '22:59:47', 'dsLat': '-23.495445', 'dsLong': '-046.484694', 'nrTemp': 33.3, 'nrBat': 3.7, 'nrSeq': 5663, 'dsArquivo': '33-20240304090930', 'cdDispositivo': 442, 'dsEndereco': 'Travessa Ramagem 10, São Paulo, Brazil'}, {'cdPosicao': 156, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.540320', 'dsLong': '-046.578923', 'nrTemp': 31.8, 'nrBat': 3.71, 'nrSeq': 5659, 'dsArquivo': '34-20240304090936', 'cdDispositivo': 442, 'dsEndereco': 'Rua Filipe Camarao 575, São Paulo, Brazil'}, {'cdPosicao': 157, 'dsModelo': 'ST410STT', 'dtData': '20240304', 'dtHora': '13:11:34', 'dsLat': '-23.492344', 'dsLong': '-046.474137', 'nrTemp': 32.4, 'nrBat': 3.66, 'nrSeq': 5767, 'dsArquivo': '35-20240304101133', 'cdDispositivo': 442, 'dsEndereco': 'Rua Antonio Pereira Simoes 362, São Paulo, Brazil'}, {'cdPosicao': 158, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.493880', 'dsLong': '-046.488923', 'nrTemp': 35.3, 'nrBat': 3.64, 'nrSeq': 5801, 'dsArquivo': '1-20240305231939', 'cdDispositivo': 442, 'dsEndereco': 'Rua Conceicao Dos Ouros 193, São Paulo, Brazil'}, {'cdPosicao': 159, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.493880', 'dsLong': '-046.488923', 'nrTemp': 36.0, 'nrBat': 3.64, 'nrSeq': 5800, 'dsArquivo': '2-20240305231945', 'cdDispositivo': 442, 'dsEndereco': 'Rua Conceicao Dos Ouros 193, São Paulo, Brazil'}, {'cdPosicao': 160, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.537895', 'dsLong': '-046.566680', 'nrTemp': 33.5, 'nrBat': 3.65, 'nrSeq': 5796, 'dsArquivo': '3-20240305231951', 'cdDispositivo': 442, 'dsEndereco': 'Rua Melo Peixoto 835, São Paulo, Brazil'}, {'cdPosicao': 161, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.537895', 'dsLong': '-046.566680', 'nrTemp': 31.4, 'nrBat': 3.65, 'nrSeq': 5793, 'dsArquivo': '4-20240305231957', 'cdDispositivo': 442, 'dsEndereco': 'Rua Melo Peixoto 835, São Paulo, Brazil'}, {'cdPosicao': 162, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.537895', 'dsLong': '-046.566680', 'nrTemp': 30.6, 'nrBat': 3.65, 'nrSeq': 5790, 'dsArquivo': '5-20240305232003', 'cdDispositivo': 442, 'dsEndereco': 'Rua Melo Peixoto 835, São Paulo, Brazil'}, {'cdPosicao': 163, 'dsModelo': 'ST410STT', 'dtData': '20240305', 'dtHora': '09:09:30', 'dsLat': '-23.501601', 'dsLong': '-046.486712', 'nrTemp': 25.5, 'nrBat': 3.65, 'nrSeq': 5786, 'dsArquivo': '6-20240305232009', 'cdDispositivo': 442, 'dsEndereco': 'Viela Deputado Albert Sabin 23, São Paulo, Brazil'}, {'cdPosicao': 164, 'dsModelo': 'ST410STT', 'dtData': '20240305', 'dtHora': '06:01:09', 'dsLat': '-23.502918', 'dsLong': '-046.488775', 'nrTemp': 27.1, 'nrBat': 3.65, 'nrSeq': 5783, 'dsArquivo': '7-20240305232015', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 165, 'dsModelo': 'ST410STT', 'dtData': '20240305', 'dtHora': '01:50:16', 'dsLat': '-23.503000', 'dsLong': '-046.488804', 'nrTemp': 30.8, 'nrBat': 3.65, 'nrSeq': 5779, 'dsArquivo': '8-20240305232021', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 166, 'dsModelo': 'ST410STT', 'dtData': '20240304', 'dtHora': '21:39:10', 'dsLat': '-23.502948', 'dsLong': '-046.488721', 'nrTemp': 39.0, 'nrBat': 3.65, 'nrSeq': 5775, 'dsArquivo': '9-20240305232027', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 167, 'dsModelo': 'ST410STT', 'dtData': '20240304', 'dtHora': '17:22:50', 'dsLat': '-23.502905', 'dsLong': '-046.488835', 'nrTemp': 43.2, 'nrBat': 3.65, 'nrSeq': 5771, 'dsArquivo': '10-20240305232033', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 191, São Paulo, Brazil'}, {'cdPosicao': 168, 'dsModelo': 'ST410STT', 'dtData': '20240306', 'dtHora': '02:21:21', 'dsLat': '-23.503265', 'dsLong': '-046.488579', 'nrTemp': 30.2, 'nrBat': 3.65, 'nrSeq': 5802, 'dsArquivo': '11-20240305232120', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 169, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.503287', 'dsLong': '-046.488582', 'nrTemp': 26.9, 'nrBat': 3.65, 'nrSeq': 5803, 'dsArquivo': '12-20240306002556', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 170, 'dsModelo': 'ST410STT', 'dtData': '20240306', 'dtHora': '04:29:20', 'dsLat': '-23.503067', 'dsLong': '-046.488717', 'nrTemp': 26.8, 'nrBat': 3.65, 'nrSeq': 5804, 'dsArquivo': '13-20240306012927', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 171, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.518290', 'dsLong': '-046.510973', 'nrTemp': 32.0, 'nrBat': 3.64, 'nrSeq': 5812, 'dsArquivo': '1-20240306095814', 'cdDispositivo': 442, 'dsEndereco': 'Avenida Amador Bueno Da Veiga 3807, São Paulo, Brazil'}, {'cdPosicao': 172, 'dsModelo': 'ST410STT', 'dtData': '20240306', 'dtHora': '11:52:45', 'dsLat': '-23.518295', 'dsLong': '-046.510975', 'nrTemp': 30.6, 'nrBat': 3.65, 'nrSeq': 5811, 'dsArquivo': '2-20240306095820', 'cdDispositivo': 442, 'dsEndereco': 'Avenida Jaime Torres 56, São Paulo, Brazil'}, {'cdPosicao': 173, 'dsModelo': 'ST410STT', 'dtData': '20240306', 'dtHora': '09:46:12', 'dsLat': '-23.502916', 'dsLong': '-046.488715', 'nrTemp': 25.6, 'nrBat': 3.65, 'nrSeq': 5809, 'dsArquivo': '3-20240306105950', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 174, 'dsModelo': 'ST410STT', 'dtData': '20240306', 'dtHora': '08:42:36', 'dsLat': '-23.504175', 'dsLong': '-046.488325', 'nrTemp': 27.9, 'nrBat': 3.65, 'nrSeq': 5808, 'dsArquivo': '4-20240306105956', 'cdDispositivo': 442, 'dsEndereco': 'Avenida Boturussu 368, São Paulo, Brazil'}, {'cdPosicao': 175, 'dsModelo': 'ST410STT', 'dtData': '20240306', 'dtHora': '07:38:52', 'dsLat': '-23.502833', 'dsLong': '-046.488561', 'nrTemp': 27.9, 'nrBat': 3.65, 'nrSeq': 5807, 'dsArquivo': '5-20240306110002', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 176, 'dsModelo': 'ST410STT', 'dtData': '20240306', 'dtHora': '06:36:20', 'dsLat': '-23.503007', 'dsLong': '-046.488656', 'nrTemp': 27.9, 'nrBat': 3.65, 'nrSeq': 5806, 'dsArquivo': '6-20240306110008', 'cdDispositivo': 442, 'dsEndereco': 'Rua Paulo Bifano Alves 301, São Paulo, Brazil'}, {'cdPosicao': 177, 'dsModelo': 'ST410STT', 'dtData': '20110102', 'dtHora': '00:03:40', 'dsLat': '-23.518290', 'dsLong': '-046.510973', 'nrTemp': 40.3, 'nrBat': 3.64, 'nrSeq': 5813, 'dsArquivo': '7-20240306110221', 'cdDispositivo': 442, 'dsEndereco': 'Avenida Amador Bueno Da Veiga 3807, São Paulo, Brazil'}]

#posicoes = (pesquisa_posicoes())

def pesquisa_usuarios():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbUsuario ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

def pesquisa_funcionarios():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT nrCodEmpregado as cdFuncionario, dsNomeEmpregado, dsEntrada, dsSaida, dsFuncao, dsEmpresa,   dsEscala, nrCargaHoraria, nrCargaHorariaMes, cdPerfil FROM DbIntelliMetrics.TbFuncionario;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  #print(selecao)
  return selecao
#print(pesquisa_funcionarios)



def pesquisa_produtos():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbProduto ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

#Produtos = (pesquisa_produtos())

def pesquisa_clientes():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbCliente ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao



def pesquisa_destinatarios():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbDestinatario ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao




def pesquisa_dispositivos():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbDispositivo ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao



def pesquisa_relacionamentos():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbRelacionamento ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

#Relacionamentos = (pesquisa_relacionamentos())

def pesquisa_tipos():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbTipo ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

#Tipos = (pesquisa_tipos())

def pesquisa_status():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbStatus ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

#Status = (pesquisa_status())

def pesquisa_unidades():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbUnidade ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

#Unidades = (pesquisa_unidades())

def pesquisa_sensores():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbSensor ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

#Sensores = (pesquisa_sensores())

def pesquisa_tags():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbTag ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

#Tags = (pesquisa_tags())



#print(Usuarios)
#print(posicoes)
#print(Clientes)
#print(Destinatarios)
#print(Dispositivos)
#print(pesquisa_produtos())
#print(Relacionamentos)
#print(Sensores)
#print(Status)
#print(Tags)
#print(Tipos)
#print(Unidades)


#def convdata(string):
#    ano = (string[0:4])
#    mes = (string[4:6])
#    dia = (string[6:8])
#    print(dia + '/' + mes + '/' + ano)

#for data in posicoes:
#    print(convdata(data['dtData']))


#convdata('20240102')
#print(dia+'/'+mes+'/'+ano)


#print(format(data, "%d/%m/%Y"))
def Inserir_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes):
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
    comando = f'insert into DbIntelliMetrics.TbFuncionario (nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes) values ("{nrCodEmpregado}", "{dsNomeEmpregado}", "{dsEntrada}", "{dsSaida}", "{cdPerfil}", "{dsFuncao}", "{dsEmpresa}", "{dsEscala}", "{nrCargaHoraria}", "{nrCargaHorariaMes}")'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

def Alterar_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes):
    conexao = conecta_bd()
    cursor = conexao.cursor()
    comando = f"update  DbIntelliMetrics.TbFuncionario set dsNomeEmpregado = '{dsNomeEmpregado}', dsEntrada = '{dsEntrada}', dsSaida = '{dsSaida}', cdPerfil = '{cdPerfil}', dsFuncao = '{dsFuncao}', dsEmpresa = '{dsEmpresa}', dsEscala = '{dsEscala}', nrCargaHoraria = '{nrCargaHoraria}', nrCargaHorariaMes = '{nrCargaHorariaMes}' where nrCodEmpregado = '{nrCodEmpregado}'"
    cursor.execute(comando)
    print(comando)
    conexao.commit()
    cursor.close()
    conexao.close()


def format_timedelta(td):
    """Format a timedelta object into a string of hours and minutes (HH:mm)."""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)  # 3600 seconds in an hour
    minutes = remainder // 60  # Get the minutes from the remainder
    return f"{hours:02}:{minutes:02}"  # Format as HH:mm






app = Flask(__name__)


#data = [{'id':'rodrigo','sobrenome':'moises'},{'id':'david','sobrenome':'paulo'}]




app.config['SECRET_KEY'] = '5160e59712d22d50e708220336549982'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

#database = SQLAlchemy(app)

users = {
    "usuario": "senha123", "rodrigo@taxidigital.net": "101275", "Yham.predilar@gmail.com": "1608@2024"
}

@app.route('/')
def home():
    return render_template('login.html', message='')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        return render_template('home.html')
    else:
        return render_template('login.html', message='Usuário ou senha inválidos!')


@app.route('/home1')
def inicio():
    #dicionario = ponto()
    return render_template("home.html")

@app.route('/contato')
def contato():
    return render_template("contato.html")

@app.route('/rel_produto_regiao')
def rel_produto_regiao():
    return render_template("rel_produto_regiao.html")

@app.route('/rel_produto_fora_destino')
def rel_produto_fora_destino():
    return render_template("rel_produto_fora_destino.html")

@app.route('/rel_produto_sintetico')
def rel_produto_sintetico():
    return render_template("rel_produto_sintetico.html")



@app.route('/map')
def map():
    return render_template("mapa_view.html")

@app.route('/mapa')
def mapa():
    start_coords = (-23.532848,-046.540013)
    folium_map = folium.Map(location=start_coords, zoom_start=10)
    posicoes = pesquisa_posicoes()

    for posicao in posicoes:
        folium.Marker([posicao['dsLat'], posicao['dsLong']]).add_to(folium_map)
        folium_map.save('templates/mapa.html')
    return render_template('map.html')


@app.route('/usuarios')
def usuarios():
    Usuarios = (pesquisa_usuarios())
    return render_template("usuarios.html", usuarios=Usuarios)

@app.route('/cadastro_clientes', methods=['GET', 'POST'])
def cadastro_clientes():
    form_cliente = FormCliente()
    Clientes = (pesquisa_clientes())
    print("oi")

    if form_cliente.validate_on_submit() and 'botao_submit_cadastrar' in request.form:
        flash(f'Cliente adicionado {form_cliente.dsNome.data}', 'alert-success')
        return redirect(url_for('cadastro_clientes'))
    return render_template("cadastro_clientes.html", form_cliente=form_cliente, clientes=Clientes)

@app.route('/cadastro_destinatarios', methods=['GET', 'POST'])
def cadastro_destinatarios():
    form_destinatario = FormDestinatario()
    Destinatarios= pesquisa_destinatarios()

    if form_destinatario.validate_on_submit() and 'botao_submit_cadastrar' in request.form:
        flash(f'Destinatario adicionado {form_destinatario.dsNome.data}', 'alert-success')
        return redirect(url_for('cadastro_destinatarios'))
    return render_template("cadastro_destinatarios.html", form_destinatario=form_destinatario, destinatarios=Destinatarios)


@app.route('/cadastro_funcionarios', methods=['GET', 'POST'])
def cadastro_funcionarios():
    form_funcionario = FuncionarioForm()
    funcionarios = pesquisa_funcionarios()
    print(funcionarios)

    if request.method == 'POST':
        i = 1
        if i == 1:

        #if form_funcionario.botao_submit_cadastrar():  # Validando se o formulário foi preenchido corretamente
            # Aqui você pegaria os dados do formulário
            print("func-ok")
            nrCodEmpregado = form_funcionario.cdFuncionario.data
            dsNomeEmpregado = form_funcionario.dsNomeEmpregado.data
            dsEntrada = form_funcionario.dsEntrada.data
            dsSaida = form_funcionario.dsSaida.data
            cdPerfil = form_funcionario.cdPerfil.data
            dsFuncao = form_funcionario.dsFuncao.data
            dsEmpresa = form_funcionario.dsEmpresa.data
            dsEscala = form_funcionario.dsEscala.data
            nrCargaHoraria = form_funcionario.nrCargaHoraria.data
            nrCargaHorariaMes = form_funcionario.nrCargaHorariaMes.data
            if 'botao_submit_cadastrar' in request.form:
                Inserir_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes)
                print(nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida)
                #return redirect(url_for('cadastro_funcionarios'))  # Redireciona para a própria página ou outra após o cadastro
                flash(f'Funcionario adicionado {form_funcionario.dsNomeEmpregado.data}', 'alert-success')
            if 'botao_submit_alterar' in request.form:
                print(nrCodEmpregado, dsNomeEmpregado)
                Alterar_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa,  dsEscala, nrCargaHoraria, nrCargaHorariaMes)

                # return redirect(url_for('cadastro_funcionarios'))  # Redireciona para a própria página ou outra após o cadastro
                flash(f'Funcionario Alterado {form_funcionario.dsNomeEmpregado.data}', 'alert-success')

            return redirect(url_for('cadastro_funcionarios'))

    return render_template('cadastro_funcionarios.html', form_funcionario=form_funcionario, funcionarios=funcionarios)
    # Passe o objeto do formulário para o template


#    if form_funcionario.validate_on_submit() and 'botao_submit_cadastrar' in request.form:
#        print("cadastrado")
#        flash(f'Funcionario adicionado {form_funcionario.dsNomeEmpregado.data}', 'alert-success')
#        return redirect(url_for('cadastro_funcionarios'))
#    return render_template("cadastro_funcionarios.html", form_funcionario=form_funcionario, funcionarios=Funcionario)




@app.route('/cadastro_usuarios', methods=['GET', 'POST'])
def cadastro_usuarios():
    form_usuario = FormUsuario()
    Usuarios = (pesquisa_usuarios())

    if form_usuario.validate_on_submit() and 'botao_submit_cadastrar' in request.form:
        flash(f'Usuario adicionado {form_usuario.dsNome.data}', 'alert-success')
        return redirect(url_for('cadastro_usuarios'))
    return render_template("cadastro_usuarios.html", form_usuario=form_usuario, Usuarios=Usuarios)

@app.route('/rel_folha_ponto')
def rel_folha_ponto():
    return render_template("rel_ponto.html")
loads = []

def converter_hora(hora):
    print("oi")
    print(hora)

    if hora == "":
        return "00:00"  # Retorna 00:00 se a hora for null
    return hora  # Se não for null, retorna a hora original


@app.route('/data', methods=['GET', 'POST', 'PUT'])
def data():
    dicionario = ponto()
    people = dicionario
    print(dicionario)
    url = "https://replit.taxidigital.net/AlteraPonto"

    if request.method == 'POST':
        print("to aqui 2")
        dados = request.get_json()
        payload = json.dumps(dados)
        print(payload)
        Horas_Array = []

        for dado in dados:
            cdPonto, cdAcessoIntelbras, c, d, dsRegistro01, dsRegistro02, g, h = dado
            #data = str(dado['dsData'] +' ' + dado['dsRegistro01'])
            dsData01 = dado['dsData'] + ' ' + converter_hora(dado['dsRegistro01'])
            dsData02 = dado['dsData'] + ' ' + converter_hora(dado['dsRegistro02'])
            #dsRegistro01 = dict(datetime.strptime(dsData01, "%d/%m/%Y %H:%M"))
            #dsRegistro02 = datetime.strptime(dsData02, "%d/%m/%Y %H:%M")
            #dsRegistro02 = datetime.strptime((dado['dsData'] + ' ' + dado['dsRegistro02']), "%d/%m/%Y %H:%M")
            #dsRegistro03 = datetime.strptime((dado['dsData'] + ' ' + dado['dsRegistro03']), "%d/%m/%Y %H:%M")
            #dsRegistro04 = datetime.strptime((dado['dsData'] + ' ' + dado['dsRegistro04']), "%d/%m/%Y %H:%M")
            #print({"dsRegistro01": dsRegistro01})
            #print(data2)

            #ponto_json = {"cdPonto": cdPonto,}
            Horas_Array.append({"cdPonto": dado['cdPonto']},)
            Horas_Array.append({"dsRegistro01": dado['dsRegistro01'], "dsRegistro02": dado['dsRegistro02']})

            print(json.dumps(Horas_Array))
            Horas_Array = []



                #cdCodigo, dsCaminho = imagem
                #imagens_array.append({"cdImagens": cdCodigo, "dsCaminho": dsCaminho})

        headers = 'Content-Type : application/json'
        #headers = {
        #    'Content-Type': 'application/json'
        #}

        #response = requests.request("PUT", url, headers=headers, data=payload)

        #print(response.text)
        #return jsonify(response)


   # if request.method == 'POST':
   #     payload = request.get_json()
   #     print(payload)
   #     return jsonify({"status": "success", "message": "Dados Atulizados !"}), 200

    return jsonify(people)

#@app.route('/')
#def index():

#    dicionario = ponto()
#    #print(dicionario)
#    #people = json.loads(dicionario)
#    #people = json.dumps(ponto())
#    #print(dicionario)

#    return render_template('base.html')





def main():
    port = int(os.environ.get("PORT", 80))
    app.run(host="192.168.15.200", port=port)


if __name__ == "__main__":
    main()



