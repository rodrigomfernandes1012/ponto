import json

from flask import Flask, request, render_template
import pandas as pd
import os
from sqlalchemy import create_engine, text

app = Flask(__name__)


# Configurações do banco de dados
DB_USER = 'admin'  # Substituir pelo seu usuário
DB_PASSWORD = 'IntelliMetr!c$'  # Substituir pela sua senha
DB_HOST = 'dbintellimetrics.c3kc6gou2fhz.us-west-2.rds.amazonaws.com'  # ou o IP do seu servidor MySQL
DB_PORT = '3306'  # Porta padrão do MySQL
DB_NAME = 'DbIntelliMetrics'  # Nome do seu banco de dados
TABLE_NAME = 'TbDadosPlanilha'  # Nome da tabela


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


@app.route('/')
def upload_form():
    return render_template('upload.html')


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

        return {'data': data_dict}, 200
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
        query = text(f"SELECT * FROM TbDadosPlanilha ORDER BY cdPlanilha DESC")  # Supondo que haja uma coluna `id` que indica a ordem
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


def main():
    port = int(os.environ.get("PORT", 80))
    app.run(host="192.168.15.200", port=port)


if __name__ == "__main__":
    main()


