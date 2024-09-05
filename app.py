import json
from io import BytesIO
from flask import Flask, request, render_template, send_file, jsonify, jsonify,  render_template,  request, redirect, flash,  url_for
import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector
import os
import json

def conecta_bd():
  conexao = mysql.connector.connect(
  host='dbintellimetrics.c3kc6gou2fhz.us-west-2.rds.amazonaws.com',
  user='admin',
  password='IntelliMetr!c$',
  database='DbIntelliMetrics')
  return conexao


# Configurações do banco de dados
DB_USER = 'admin'  # Substituir pelo seu usuário
DB_PASSWORD = 'IntelliMetr!c$'  # Substituir pela sua senha
DB_HOST = 'dbintellimetrics.c3kc6gou2fhz.us-west-2.rds.amazonaws.com'  # ou o IP do seu servidor MySQL
DB_PORT = '3306'  # Porta padrão do MySQL
DB_NAME = 'DbIntelliMetrics'  # Nome do seu banco de dados
TABLE_NAME = 'TbDadosPlanilha'  # Nome da tabela





app = Flask(__name__)


banco_url = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

COLUMN_MAPPING = {
    'NF': 'dsNF',
    'Ordem Recebimento': 'dsOrdemRec',
    'CÓDIGO': 'dsCodigo',
    'DESCRIÇÃO': 'dsDescricao',
    'QTD NF': 'nrQtde',
    'SO': 'dsSO',
    'LINHA': 'nrLinha',
    'QUANTIDADE DE CAIXAS': 'nrQtdeCaixas',
    'QTD RECEBIDA (PEÇAS)': 'nrQtdeRecPecas',
    'NUMERO DE SERIE': 'dsNumeroSerie',
    'PESO': 'nrPeso',
    'DIMENSÕES': 'dsDimensoes',
    'LOCALIZAÇÃO': 'dsLocalizacao',
    'OBS OPERAÇÃO': 'dsObs',
    'SO + LINHA': 'dsSoLinha',
    'TIPO Armazenagem': 'dsTipoArmazenagem',
    'Nome da Planilha': 'dsNomePlanilha'  # Adicionando o campo nome_da_planilha
}




@app.route('/cubagem', methods=['POST'])
def cubagem():
    dados = request.get_json()
    payload = json.dumps(dados)
    print(dados)
    return ({'message': 'Peso recebido com sucesso', 'peso': dados}), 200


@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/get_planilhas', methods=['GET'])
def get_planilhas():
    db_connection = conecta_bd()
    cursor = db_connection.cursor()
    cursor.execute("SELECT DISTINCT dsNomePlanilha FROM TbDadosPlanilha")
    results = cursor.fetchall()
    planilhas = [row[0] for row in results]
    cursor.close()
    db_connection.close()
    print(planilhas)
    return jsonify(planilhas)


def download_planilha():
    planilha_selecionada = request.json['planilha']
    print(planilha_selecionada)
    db_connection = conecta_bd()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM TbDadosPlanilha WHERE dsNomePlanilha = %s", (planilha_selecionada,))
    dados = cursor.fetchall()
    cursor.close()
    db_connection.close()

    # Criando um DataFrame com os dados
    df = pd.DataFrame(dados)
    print(dados)

    # Usando BytesIO para criar um buffer de memória
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl', sheet_name='Dados')

    # Rewind the buffer
    output.seek(0)

    return send_file(output,
                     attachment_filename=planilha_selecionada,
                     as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado', 400

    file = request.files['file']

    if file.filename == '':
        return 'Arquivo não selecionado', 400

    try:
        # Lê a planilha do Excel
        df = pd.read_excel(file)
        print(file.filename)

        # Adiciona uma nova coluna com o nome da planilha
        nome_planilha = file.filename
        df['Nome da Planilha'] = nome_planilha

        # Rename columns based on COLUMN_MAPPING
        df.rename(columns=COLUMN_MAPPING, inplace=True)

        # Converte o DataFrame para um dicionário
        data_dict = df.to_dict(orient='records')


        # Conectar ao banco de dados e gravar dados
        gravar_dados_no_banco(df)
        return redirect(url_for('mostrar_dados'))
        #return {'data': data_dict}, 200
    except Exception as e:
        return str(e), 400


@app.route('/dados', methods=['GET'])
def mostrar_dados():
    try:
        # Cria a string de conexão com o banco de dados MySQL
        banco_url = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

        # Cria a conexão com o banco de dados
        engine = create_engine(banco_url)

        # Faz uma consulta para selecionar os dados ordenados pela data mais recente
        query = text(f"SELECT distinct dsNF, dsOrdemRec, dsCodigo, dsDescricao, nrQtde, dsSO, nrLinha, nrQtdeCaixas, nrQtdeRecPecas, dsNumeroSerie, nrPeso, dsDimensoes, dsLocalizacao, dsObs, dsSoLinha, dsTipoArmazenagem, dsNomePlanilha FROM DbIntelliMetrics.TbDadosPlanilha order by cdPlanilha desc")  # Supondo que haja uma coluna `id` que indica a ordem
        with engine.connect() as conn:
            result = conn.execute(query)
            dados = result.fetchall()

        return render_template('dados.html', dados=dados)
    except Exception as e:
        return str(e), 400


def gravar_dados_no_banco(df):
    # Cria a string de conexão com o banco de dados MySQL
    banco_url = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # Cria a conexão com o banco de dados
    engine = create_engine(banco_url)

    # Insere os dados na tabela, substituindo os dados existentes ou adicionando
    df.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False)

@app.route('/export', methods=['POST'])
def export_data():
    json_data = request.json
    dados = json_data['dados']  # Os dados recebidos aqui
    df = pd.DataFrame(dados)

    # Usando BytesIO para criar um buffer de memória
    output = BytesIO()
    # Exportando para Excel
    df.to_excel(output, index=False, engine='openpyxl', sheet_name='Dados')

    # Rewind the buffer
    output.seek(0)

    # Enviando o arquivo
    return send_file(output, download_name="planilha", mimetype='xlsx', as_attachment=True)

def main():
    port = int(os.environ.get("PORT", 80))
    app.run(host="192.168.15.200", port=port)


if __name__ == "__main__":
    main()


