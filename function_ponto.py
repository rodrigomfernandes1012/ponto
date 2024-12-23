from datetime import datetime, time
from io import BytesIO
from flask import Flask, jsonify,  render_template,  request, redirect, flash,  url_for, send_file, send_from_directory
import mysql.connector
from forms import FormCliente, FormDestinatario, FormUsuario, FuncionarioForm
import requests
#import qrcode
#import pybase64
import pandas as pd
from sqlalchemy import create_engine, text, exc
import re
import mysql.connector
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import date






##Configuração do dispositivo
ip = '201.92.45.49:8090'
username = 'admin'
password = 'Start010'


COLUMN_MAPPING = {
    'RECEBIMENTO WMS': 'nrRecWms',
    'Ordem Recebimento': 'dsOrdemRec',
    'linha': 'nrLinha',
    'CÓDIGO': 'dsCodigo',
    'DESCRIÇÃO': 'dsDescricao',
    'QTD NF':'nrQtdeNf',
    'SO': 'dsSO',
    'ITEM': 'dsItem',
    'QUANTIDADE DE CAIXAS': 'nrQtdeCaixas',
    'QTD RECEBIDA (PEÇAS)': 'nrQtdeRecebida',
    'PESO': 'nrPeso',
    'DIMENSÕES': 'dsDimensoes',
    'LOCALIZAÇÃO': 'dsLocalizacao',
    'OBS OPERAÇÃO': 'dsObsOpe',
    'QUANTIDADE DE PALLET': 'nrQtdePallet',
    'STATUS': 'dsStatus',
    'Nome da Planilha': 'dsNomePlanilha'  # Adicionando o campo nome_da_planilha
}







token = "8c4EF9vXi8TZe6581e0af85c25"

def conecta_bd():
  conexao = mysql.connector.connect(
  host='dbintellimetrics.c3kc6gou2fhz.us-west-2.rds.amazonaws.com',
  user='admin',
  password='IntelliMetr!c$',
  database='DbIntelliMetrics')
  return conexao

def substituir_caracteres(s):
    """
    Substitui os caracteres ':', ';', '-', e espaço por vazio em uma string.

    :param s: A string de entrada.
    :return: A string com os caracteres substituídos.
    """
    # Define a expressão regular para capturar os caracteres desejados
    pattern = r'[:;\-\s]'

    # Use re.sub para substituir todos os caracteres correspondentes por vazio
    resultado = re.sub(pattern, '', s)

    return resultado




class IntelbrasAccessControlAPI:
    def __init__(self, ip: str, username: str, passwd: str):
        self.ip = ip
        self.username = username
        self.passwd = passwd
        self.digest_auth = requests.auth.HTTPDigestAuth(self.username, self.passwd)

    def delete_all_users_v2(self) -> str:
        '''
        This command delete all user and credential incluse in device
        '''
        try:
            url = "http://{}/cgi-bin/AccessUser.cgi?action=removeAll".format(
                str(self.ip)
            )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Remove All Users using V2 command - ", e)


    def add_user_v2(self, CardName: str, UserID: int, UserType: int, Password: int, Authority: int, Doors: int,
                    TimeSections: int, ValidDateStart: str, ValidDateEnd: str):
        UserList = (

                '''{
                        "UserList": [
                            {
                            "UserID": "''' + str(UserID) + '''",
                            "UserName": "''' + str(CardName) + '''",
                            "UserType": ''' + str(UserType) + ''',
                            "Authority": ''' + str(Authority) + ''',
                            "Password": "''' + str(Password) + '''",
                            "Doors": ''' + '[' + str(Doors) + ']' + ''',
                            "TimeSections": ''' + '[' + str(TimeSections) + ']' + ''',
                            "ValidFrom": "''' + str(ValidDateStart) + '''",
                            "ValidTo": "''' + str(ValidDateEnd) + '''"
                        }
                    ]
                }''')
        try:
            url = "http://{}/cgi-bin/AccessUser.cgi?action=insertMulti".format(
                str(self.ip),
            )
            result = requests.get(url, data=UserList, auth=self.digest_auth, stream=True, timeout=20,
                                  verify=False)  # noqa
            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("deu pau - During Add New User using V2 command - ")

    def update_user_v2(self, CardName: str, UserID: int, UserType: int, Password: int, Authority: int, Doors: int,
                       TimeSections: int, ValidDateStart: str, ValidDateEnd: str) -> str:
        UserList = (

                '''{
                        "UserList": [
                            {
                                "UserName": "''' + str(CardName) + '''",
                            "UserID": "''' + str(UserID) + '''",
                            "UserType": ''' + str(UserType) + ''',
                            "Password": "''' + str(Password) + '''",
                            "Authority": "''' + str(Authority) + '''",
                            "Doors": "''' + '[' + str(Doors) + ']' + '''",
                            "TimeSections": "''' + '[' + str(TimeSections) + ']' + '''",
                            "ValidFrom": "''' + str(ValidDateStart) + '''",
                            "ValidTo": "''' + str(ValidDateEnd) + '''"
                        }
                    ]
                }''')
        try:
            url = "http://{}/cgi-bin/AccessUser.cgi?action=updateMulti".format(
                str(self.ip),
            )

            result = requests.get(url, data=UserList, auth=self.digest_auth, stream=True, timeout=20,
                                  verify=False)  # noqa
            #print("result.text")
            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Update User using V2 command - ")

    def get_all_users(self, count: int) -> dict:
        try:
            url = "http://{}/cgi-bin/recordFinder.cgi?action=doSeekFind&name=AccessControlCard&count={}".format(
                str(self.ip),
                str(count),
            )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users")

    def get_users_count(self) -> dict:
        try:
            url = "http://{}/cgi-bin/recordFinder.cgi?action=getQuerySize&name=AccessUserInfo".format(
                str(self.ip),
            )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users Count")

    def get_user_cardno(self, CardNoList: str) -> dict:
        try:
            url = "http://{}/cgi-bin/AccessCard.cgi?action=list&CardNoList[0]={}".format(
                str(self.ip),
                str(CardNoList).upper(),
            )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users CardNo")

    def get_user_recno(self, recno: int) -> dict:
        try:
            url = "http://{}/cgi-bin/recordUpdater.cgi?action=get&name=AccessControlCard&recno={}".format(
                str(self.ip),
                str(recno),
            )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users RecNo")

    def get_user_id(self, UserIDList: int) -> dict:
        try:
            url = "http://{}/cgi-bin/AccessUser.cgi?action=list&UserIDList[0]={}".format(
                str(self.ip),
                str(UserIDList),
            )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users Id")


    def set_remove_users_id(self, UserIDList: int) -> dict:
        try:
            url = "http://{}/cgi-bin/AccessUser.cgi?action=removeMulti&UserIDList[0]={}".format(
                str(self.ip),
                str(UserIDList),
            )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Remove Users By ID")

    def add_card_v2(self, UserID: int, CardNo: int, CardType: int, CardStatus: int) -> dict:
        '''
        UserID: ID do usuário
        CardNo: Número do cartão
        CardType: Tipo do Cartão; 0- Ordinary card; 1- VIP card; 2- Guest card; 3- Patrol card; 4- Blocklist card; 5- Duress card
        CardStatus: Status do Cartão; 0- Normal; 1- Cancelado; 2- Congelado
        '''
        CardList = (

                '''{
                        "CardList": [
                            {
                                "UserID": "''' + str(UserID) + '''",
                            "CardNo": "''' + str(CardNo) + '''",
                            "CardType": ''' + str(CardType) + ''',
                            "CardStatus": "''' + str(CardStatus) + '''"
                        }
                    ]
                }''')


        url = "http://{}/cgi-bin/AccessCard.cgi?action=insertMulti".format(
            str(self.ip),
            str(UserID),
            str(CardNo).upper(),
            str(CardType),
            str(CardStatus),
        )
        result = requests.post(url, data=CardList, auth=self.digest_auth, stream=True, timeout=20,
                               verify=False)  # noqa




    def _raw_to_dict(self, raw):
        data = {}
        for i in raw:
            if len(i) > 1:
                name = i[:i.find("=")]
                val = i[i.find("=") + 1:]
                try:
                    len(data[name])
                except:
                    data[name] = val
            else:
                data["NaN"] = "NaN"
        return data



api = IntelbrasAccessControlAPI(ip, username, password)


def le_arquivo():
    try:
        print("entrei na função")
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'CadastroFun.txt')
        with (open(filename, "r") as arquivo):
            print("abrindo arquivo")
            linhas = arquivo.readlines()
            for linha in linhas:

                nrCodEmpregado = (linha[0:6])
                dsNomeEmpregado = (linha[6:86])
                dsLogradouro = (linha[86:136])
                dsNumCasa = (linha[136:141])
                dsComplemento = (linha[141:156])
                dsBairro = (linha[156:176])
                dsCidade = (linha[176:196])
                dsFuncao = (linha[560:610])
                dsPis = (linha[798:821])
                dsCpf = int(linha[763:774])
                dsSenha = int(linha[763:766])
                dsEmpresa = ("Predilar Soluções")
                dsEntrada = ("00:00")
                dsSaida = ("00:00")
                cdPerfil = 1
                dsEscala = (linha[421:424])
                nrCargaHoraria = 44
                nrCargaHorariaMes = 220
                dsCelular =""
                dsEmail="@"
                dsUser = username
                dtRegistro = datetime.now().strftime("%d/%m/%Y")
                #print(nrCodEmpregado)
                #print(dsNomeEmpregado)
                #print(dsLogradouro)
                #print(dsNumCasa)
                #print(dsComplemento)
                #print(dsBairro)
                #print(dsCidade)
                #print(dsFuncao)
                #print(dsPis)
                #print(dsCpf)
                #print(arquivo.name)
                #print(linha)
                Inserir_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsCpf, dsLogradouro, dsNumCasa, dsComplemento, dsBairro, dsCidade, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsPis, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes, dsCelular, dsEmail, dsUser)
                api.add_user_v2(dsNomeEmpregado, dsCpf, 0, dsSenha, 2, 0, 255, '2024-10-15 00:10:00', '2030-01-01 00:00:00')
                api.add_card_v2(dsCpf, dsCpf, 0, 0)
                print(dsNomeEmpregado)
                print('cadastrado com sucesso!')
        return {"message": "Cadastrados com sucesso !"}
    except Exception as e:
        return {"error": f"Não foi possivel cadastrar, tente mais tarde ou ligue para o suporte {e}"}


def inserir_tb_funcionario(
        dsBairro,
        dsCidade,
        dsComplemento,
        dsFuncao,
        dsLogradouro,
        dsNomeEmpregado,
        dsNumCasa,
        dsUser,
        dtRegistro,
        nrCodEmpregado,
        TbFuncionariocol,
):
    # Conecta ao banco de dados
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Verifica se o registro já existe
        verifica_comando = """
            SELECT 1 FROM DbIntelliMetrics.TbFuncionario
            WHERE nrCodEmpregado = %s
        """
        cursor.execute(verifica_comando, (nrCodEmpregado,))
        resultado = cursor.fetchone()

        if resultado:
            print("Empregado já existe com nrCodEmpregado:", nrCodEmpregado)
            return

        # Prepara o comando de inserção
        comando = """
            INSERT INTO DbIntelliMetrics.TbFuncionario (
                dsBairro, dsCidade, dsComplemento, dsFuncao, dsLogradouro,
                dsNomeEmpregado, dsNumCasa, dsUser, dtRegistro, nrCodEmpregado, TbFuncionariocol
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            dsBairro, dsCidade, dsComplemento, dsFuncao, dsLogradouro,
            dsNomeEmpregado, dsNumCasa, dsUser, dtRegistro, nrCodEmpregado, TbFuncionariocol
        )

        # Executa a inserção
        cursor.execute(comando, valores)
        conexao.commit()
        print("Registro inserido com sucesso.")

    except Exception as e:
        print("Ocorreu um erro ao inserir o registro:", e)

    finally:
        # Fecha a conexão com o banco de dados
        cursor.close()
        conexao.close()


# Exemplo de uso
# inserir_tb_funcionario("Bairro Exemplo", "Cidade Exemplo", ... , 123)



def get_today_data():
    connection = conecta_bd()
    cursor = connection.cursor(dictionary=True)
    print('Conectado ao banco de')

    try:
        today = date.today().isoformat()  # Formato padrão YYYY-MM-DD
        print(today)

        query = "SELECT cdPonto, dsCardName, dsRegistroAut, dsRegistro01, dsRegistro02, dsRegistro03, dsRegistro04, dsTipoRegistro, dsObservacao FROM DbIntelliMetrics.TbPonto   WHERE dsRegistroAut =" + today
        print(query)
        cursor.execute(query)
        result = cursor.fetchall()

        print(result)
        return jsonify(result)

    except mysql.connector.Error as err:

        return jsonify({"error": str(err)})

    finally:
        cursor.close()
        connection.close()

def Selecionar_TbPonto():
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
    comando = f"select cdPonto,  TRIM(dsCardName) as dsCardName,  DATE_FORMAT(STR_TO_DATE(dsRegistroAut, '%Y-%m-%d %H:%i:%s'), '%d/%m/%Y') AS dsData, DATE_FORMAT(STR_TO_DATE(dsRegistro01, '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d %H:%i') AS dsRegistro00,  DATE_FORMAT(STR_TO_DATE(dsRegistro01, '%Y-%m-%d %H:%i:%s'), '%H:%i') AS dsRegistro01, DATE_FORMAT(STR_TO_DATE(dsRegistro02, '%Y-%m-%d %H:%i:%s'), '%H:%i') AS dsRegistro02, DATE_FORMAT(STR_TO_DATE(dsRegistro03, '%Y-%m-%d %H:%i:%s'), '%H:%i') AS dsRegistro03, DATE_FORMAT(STR_TO_DATE(dsRegistro04, '%Y-%m-%d %H:%i:%s'), '%H:%i') AS dsRegistro04, dsTipoRegistro, dsObservacao  from DbIntelliMetrics.TbPonto  order by dsCardName asc, dsRegistroAut asc ;"
    print(comando)
    cursor.execute(comando)
    resultado = cursor.fetchall()
    #print(resultado)
    cursor.close()
    conexao.close()
    return resultado





#def ponto():
#    url = "https://replit.taxidigital.net/Ponto"
#    payload = {}
#    headers = {}
#    response = requests.request("GET", url, headers=headers, data=payload)
#    selecao = json.loads(response.text)
#    print(selecao)

#    dados_dicionario = {}

#    for registro in selecao:
#        nome = registro['dsCardName']
#        dados_dicionario[nome] = []
#        dados_dicionario[nome] = [data]
#        dados_dicionario[nome].append(data)
#        return selecao

#def get_ponto():
#  conexao = conecta_bd()
#  cursor = conexao.cursor(dictionary=True)
#  comando = f'SELECT * FROM DbIntelliMetrics.TbAcessoIntelBras where dsStatus = 1 and dsUtc >= 1722502193 ;'
#  cursor.execute(comando)
#  selecao = cursor.fetchall() # ler o banco de dados
#  dados_dicionario = {}

#  for registro in selecao:
#      nome = registro['dsCardName']

#      datacompleta = int(registro['dsUtc'])
#      data = (datetime.utcfromtimestamp(datacompleta).strftime('%d-%m-%Y'))
#      dados_dicionario[nome] = []
#      dados_dicionario[nome] = [data]
#      dados_dicionario[nome].append(data)
#  cursor.close()
#  conexao.close()
#  return selecao

#def getponto():
#    conexao = conecta_bd()
#    cursor = conexao.cursor(dictionary=True)
#    comando = f'SELECT dsCardNo FROM DbIntelliMetrics.TbAcessoIntelBras where dsStatus = 1 and dsutc >=1722506000 group by dsCardNo, dsCardName order by dsCardname;'
#    cursor.execute(comando)
#    funcionarios = cursor.fetchall()
#    cursor.close()
#    conexao.close()
#    # Array para armazenar os resultados
#    funcionarios_json = []

#    for funcionario in funcionarios:
#        (
#            dsCardNo,
#        ) = funcionario
#        dsCardNo = (funcionario['dsCardNo'])
#        funcionarios_json.append(funcionario)
#        conexao = conecta_bd()
#        cursor = conexao.cursor(dictionary=True)
#        comando = f'SELECT dsUtc FROM DbIntelliMetrics.TbAcessoIntelBras where dsStatus = 1 and dsutc >=1722506000  and dsCardNo = {dsCardNo};'
#        cursor.execute(comando)
#        datas = cursor.fetchall()
#        cursor.close()
#        conexao.close()
def Alterar_TbPonto(cdPonto, dsRegistro01, dsRegistro02, dsRegistro03, dsRegistro04, dsData, dsTipoRegistro, dsObservacao ):
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
    comando = f"update DbIntelliMetrics.TbPonto set dsRegistro01 = STR_TO_DATE('{dsData} {dsRegistro01}', '%d/%m/%Y %H:%i'), dsRegistro02 = STR_TO_DATE('{dsData} {dsRegistro02}', '%d/%m/%Y %H:%i'),dsRegistro03 = STR_TO_DATE('{dsData} {dsRegistro03}', '%d/%m/%Y %H:%i'), dsRegistro04 = STR_TO_DATE('{dsData} {dsRegistro04}', '%d/%m/%Y %H:%i'), dsTipoRegistro = '{dsTipoRegistro}', dsObservacao = '{dsObservacao}' where cdPonto = '{cdPonto}'"
    print(comando)
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

def gravar_dados_no_banco(df):

 # Configurações de conexão com o banco de dados MySQL
    banco_url = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    print("to_aqui ?")
# Cria a conexão com o banco de dados
    engine = create_engine(banco_url)

    try:
        # Checa se a tabela já existe, e lê o esquema
        query = f"SELECT * FROM {TABLE_NAME} LIMIT 0"
        current_df = pd.read_sql(query, con=engine)
        print(current_df)
        print(query)

        # Garante que os DataFrames têm as mesmas colunas
        for column in current_df.columns.difference(df.columns):
            df[column] = None  # Coloca NaNs nas colunas que faltam no novo df
            # Remove caracteres indesejados do campo 'dsCodigoLote'
            if 'dsCodigoLote' in df.columns:
                df['dsCodigoLote'] = df['dsCodigoLote'].str.replace(';', '', regex=True) \
                    .str.replace('-', '', regex=True) \
                    .str.replace(':', '', regex=True) \
                    .str.replace(' ', '', regex=True)

        # Insere os dados na tabela
        df.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False)
    except exc.SQLAlchemyError as e:
        print(f"Error on inserting data: {str(e)}")









def pesquisa_usuarios():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbUsuario ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

def pesquisa_planilha():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT *  FROM DbIntelliMetrics.TbDadosPlanilha order by dsSO, cdTbDadosPlanilha ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

def update_st_impresso(ds_id_list):
    for ds_id in ds_id_list['dsId']:
        conexao = conecta_bd()
        cursor = conexao.cursor(dictionary=True)
        query = "UPDATE TbDadosPlanilha SET stImpresso = 1 WHERE stImpresso = 0 and  cdTbDadosPlanilha = %s"
        cursor.execute(query, (ds_id,))
        print(f"Atualizado stImpresso para 1 para o ID: {ds_id}")

        # Confirma as mudanças no banco de dados
        conexao.commit()
        print("Atualizações concluídas.")



def pesquisa_funcionarios():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT nrCodEmpregado as cdFuncionario, dsNomeEmpregado, dsCpf,  dsCelular, dsEmail,  dsEntrada, dsSaida, dsFuncao, dsEmpresa,   dsEscala, nrCargaHoraria, nrCargaHorariaMes, cdPerfil FROM DbIntelliMetrics.TbFuncionario;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

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

def pesquisa_status():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbStatus ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  cursor.close()
  conexao.close()
  return selecao

def Inserir_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsCpf, dsLogradouro, dsNumCasa, dsComplemento, dsBairro, dsCidade, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsPis, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes, dsCelular, dsEmail, dsUser):
        # Conectar ao banco de dados
        conexao = conecta_bd()
        cursor = conexao.cursor(dictionary=True)

        try:
            # Verificar se o registro já existe
            verifica_comando = """
                SELECT 1 FROM DbIntelliMetrics.TbFuncionario
                WHERE nrCodEmpregado = %s
            """
            cursor.execute(verifica_comando, (nrCodEmpregado,))
            resultado = cursor.fetchone()

            if resultado:
                print("Empregado já existe com nrCodEmpregado:", nrCodEmpregado)
                return

            # Preparar o comando de inserção
            comando = """
                INSERT INTO DbIntelliMetrics.TbFuncionario (nrCodEmpregado, dsNomeEmpregado, dsCpf, dsLogradouro, dsNumCasa, dsComplemento, dsBairro, dsCidade, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsPis, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes, dsCelular, dsEmail, stStatus, dsUser)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)
            """
            valores = (
                nrCodEmpregado, dsNomeEmpregado, dsCpf, dsLogradouro, dsNumCasa, dsComplemento, dsBairro, dsCidade,
                dsEntrada, dsSaida, cdPerfil, dsFuncao, dsPis, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes,
                dsCelular, dsEmail, 1, dsUser
            )

            # Executar inserção
            cursor.execute(comando, valores)
            print(comando,valores)
            conexao.commit()
            print("Registro inserido com sucesso.")

        except Exception as e:
            print("Ocorreu um erro ao inserir o registro:", e)

        finally:
            # Fechar o cursor e a conexão com o banco de dados
            cursor.close()
            conexao.close()

    # Exemplo de uso
    # inserir_tb_funcionario(1, "Nome Exemplo", "08:00", "17:00", 1, "Função", "Empresa", "Escala", 40, 160, "999999999", "email@example.com")


def Alterar_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsCpf, dsEmail, dsCelular, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes):
    conexao = conecta_bd()
    cursor = conexao.cursor()
    comando = f"update  DbIntelliMetrics.TbFuncionario set dsNomeEmpregado = '{dsNomeEmpregado}', dsCpf = '{dsCpf}', dsEmail = '{dsEmail}', dsCelular = '{dsCelular}' , dsEntrada = '{dsEntrada}', dsSaida = '{dsSaida}', cdPerfil = '{cdPerfil}', dsFuncao = '{dsFuncao}', dsEmpresa = '{dsEmpresa}', dsEscala = '{dsEscala}', nrCargaHoraria = '{nrCargaHoraria}', nrCargaHorariaMes = '{nrCargaHorariaMes}' where nrCodEmpregado = '{nrCodEmpregado}'"
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

def Excluir_TbFuncionario(dsCpf):
    conexao = conecta_bd()
    cursor = conexao.cursor()
    comando = f"delete from  DbIntelliMetrics.TbFuncionario where dsCpf = '{dsCpf}'"
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()


def Inserir_TbLog(dsTbAcesso, dsAcao, dsIp,  dsLogin):
    print(dsTbAcesso, dsAcao, dsIp,  dsLogin)
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
    comando = f'insert into DbIntelliMetrics.TbLog (dsTbAcesso, dsAcao, dsIp, dsLogin) values ("{dsTbAcesso}", "{dsAcao}", "{dsIp}", "{dsLogin}")'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()
    username = dsLogin
    return username


def separar_dados(texto):
    # Usar expressão regular para separar o texto por ;, / ou -
    import re
    dados = re.split(r'[;/-]', texto)

    # Retornar as duas primeiras partes separadas
    if len(dados) >= 2:
        return dados[0].strip(), dados[1].strip()  # Remove espaços desnecessários
    else:
        return dados[0].strip(), 0  # Remove espaços desnecessários


def Update_TbDadosPlanilha(dados):
    agora = datetime.now()
    dsEtiqueta = dados.get('xEtiqueta')
    dsSo, dsItem = separar_dados(dsEtiqueta)
    dsItem = int(dsItem)

    nrPeso = float(dados.get('nPeso', 0))  # Convertendo para float e definindo um padrão
    nrQtd = 1
    nrAlt = float(dados.get('nAlt', 0))  # Convertendo para float
    nrLarg = float(dados.get('nLarg', 0))  # Convertendo para float
    nrComp = float(dados.get('nComp', 0))  # Convertendo para float

    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)

    # Obter a quantidade total de nrQtdeRecebida
    cursor.execute(
        "SELECT SUM(nrQtdeRecebida) AS totalQtdeRecebida "
        "FROM DbIntelliMetrics.TbDadosPlanilha WHERE dsSO = %s AND dsItem = %s",
        (dsSo, dsItem)
    )
    resultado_total = cursor.fetchone()
    totalQtdeRecebida = resultado_total['totalQtdeRecebida'] if resultado_total['totalQtdeRecebida'] is not None else 0

    # Consultar dados existentes
    cursor.execute(
        "SELECT dsSO, dsItem, nrQtdeRecebida, nrQtdeCaixas, nrPeso, dsDimensoes, nrRecWms, dsOrdemRec, "
        "nrLinha, dsCodigo, dsDescricao, nrQtdeNf, dsLocalizacao, dsObsOpe, nrQtdePallet "
        "FROM DbIntelliMetrics.TbDadosPlanilha WHERE dsSO = %s AND dsItem = %s",
        (dsSo, dsItem)
    )
    resultados = cursor.fetchall()

    if any(resultado['dsDimensoes'] is None for resultado in resultados):
        # Se encontrar, faz UPDATE
        comando = """
            UPDATE DbIntelliMetrics.TbDadosPlanilha 
            SET nrQtdeRecebida = %s, 
                nrPeso = %s, 
                dsDimensoes = CONCAT(%s, ' x ', %s, ' x ', %s), 
                nrQtdeCaixas = %s, 
                dsStatus = 'Atualizado' 
            WHERE dsSO = %s AND dsItem = %s
        """
        cursor.execute(comando, (nrQtd, nrPeso, nrAlt, nrComp, nrLarg, 1, dsSo, dsItem))
        Inserir_TbLog("TbDadosPlanilha", "Update_Cubagem", dsSo, dsItem)
    else:
        if resultados:
            ultimo_resultado = resultados[0]  # Pega o primeiro resultado
            nrRecWms = ultimo_resultado['nrRecWms']
            dsOrdemRec = ultimo_resultado['dsOrdemRec']
            nrLinha = ultimo_resultado['nrLinha']
            dsCodigo = ultimo_resultado['dsCodigo']
            dsDescricao = ultimo_resultado['dsDescricao']
            nrQtdeNf = ultimo_resultado['nrQtdeNf']
            nrQtdeCaixas = 1
            dsLocalizacao = ultimo_resultado['dsLocalizacao']
            dsObsOpe = ultimo_resultado['dsObsOpe']
            nrQtdePallet = ultimo_resultado['nrQtdePallet']

            comando = """
                INSERT INTO DbIntelliMetrics.TbDadosPlanilha 
                (dsSO, dsItem, nrQtdeRecebida, nrPeso, dsDimensoes, nrRecWms, dsOrdemRec, nrLinha, 
                 dsCodigo, dsDescricao, nrQtdeNf, nrQtdeCaixas, dsLocalizacao, dsObsOpe, nrQtdePallet, dsStatus) 
                VALUES 
                (%s, %s, %s, %s, CONCAT(%s, ' x ', %s, ' x ', %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Inserido')
            """
            print("01")
            print(comando)
            cursor.execute(comando, (
                dsSo, dsItem, nrQtd, nrPeso, nrAlt, nrComp, nrLarg,
                nrRecWms, dsOrdemRec, nrLinha, dsCodigo, dsDescricao,
                nrQtdeNf, nrQtdeCaixas, dsLocalizacao, dsObsOpe, nrQtdePallet
            ))
        else:
            # Se não houver resultados, insere um registro padrão
            comando = """
                INSERT INTO DbIntelliMetrics.TbDadosPlanilha 
                (dsSO, dsItem, nrQtdeRecebida, nrPeso, dsDimensoes, nrRecWms, dsOrdemRec, nrLinha, 
                 dsCodigo, dsDescricao, nrQtdeNf, nrQtdeCaixas, dsLocalizacao, dsObsOpe, nrQtdePallet, dsStatus) 
                VALUES 
                (%s, %s, %s, %s, CONCAT(%s, ' x ', %s, ' x ', %s), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Não Localizado')
            """
            print("02")
            print(comando)
            cursor.execute(comando, (
                dsSo, dsItem, nrQtd, nrPeso, nrAlt, nrComp, nrLarg
            ))

        Inserir_TbLog("TbDadosPlanilha", "Insert_Cubagem", dsSo, dsItem)

    # Commit e fechamento da conexão
    conexao.commit()
    cursor.close()
    conexao.close()

    return "Cadastrado com sucesso"





def obter_ip_publico():
    # Verifica o cabeçalho X-Forwarded-For
    ip = request.headers.get('X-Forwarded-For')
    if ip:
        # O X-Forwarded-For pode retornar uma lista de IPs; pegamos o primeiro
        ip = ip.split(',')[0]
    else:
        # Se não houver X-Forwarded-For, pega o remote_addr
        ip = request.remote_addr

    return ip
def cria_qr(dsCpf):

    valor =str(dsCpf)
    vtipo = '.png'
    imagem = qrcode.make(valor)
    imagem.save("QrCode" + vtipo)

def cria_base64(arquivo):
    with open( arquivo, "rb") as img_file:
        my_string = pybase64.b64encode(img_file.read())
        img_cliente = (my_string.decode('utf-8'))
        return img_cliente


def EnviaImgWhats(ArquivoBase64, dsCelular):
    url = "https://app.whatsgw.com.br/api/WhatsGw/Send"
    dicionario = {
        "apikey": "fea4fe42-3cd6-4002-bd33-31badb5074dc",
        "phone_number": "5511945480370",
        "check_status": "1",
        "message_custom_id": "Start",
        "message_type": "image",
        "message_body_mimetype": "image/jpeg",
        "message_body_filename": "QrCode.png",
        "message_caption": "Use este QR para registrar o seu ponto\nObrigado\n*Predilar*", }
    dicionario["message_body"] = ArquivoBase64
    dicionario["contact_phone_number"] = dsCelular
    payload = json.dumps(dicionario)
    print(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text



def send_email(subject, body, to_email, from_email, password, smtp_server='smtp.gmail.com', smtp_port=587):
    """
    Sends an email with an attachment using the specified SMTP server.

    :param subject: Subject of the email.
    :param body: Body of the email.
    :param to_email: Recipient email address.
    :param from_email: Sender email address (must match the authenticated user).
    :param password: Password for the sender email account.
    :param smtp_server: SMTP server address.
    :param smtp_port: SMTP server port.
    """
    # Create the email header
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Specify the attachment file and path
    filename = 'QrCode.png'
    filepath = os.path.join(os.getcwd(), filename)  # Assumes the file is in the current working directory

    try:
        # Open the file to be sent
        with open(filepath, 'rb') as attachment:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(mime_base)

        # Add header as key/value pair to attachment part
        mime_base.add_header('Content-Disposition', f'attachment; filename={filename}')

        # Attach the file to the email
        msg.attach(mime_base)

        # Set up the server connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Log in to the account
        server.login(from_email, password)

        # Send the email
        server.send_message(msg)
        print(f"Email sent successfully to {to_email}")

    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
    finally:
        server.quit()

login_usuario = None
dsIp = None
