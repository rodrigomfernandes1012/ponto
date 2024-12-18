#from flask import Flask, jsonify,  render_template,  request, redirect, flash,  url_for, send_file
from PIL import ImageGrab

from function_ponto import *
from function import *


ip = '201.92.45.49:8090'
username = 'admin'
password = 'Start010'




# Configurações do banco de dados
DB_USER = 'admin'  # Substituir pelo seu usuário
DB_PASSWORD = 'IntelliMetr!c$'  # Substituir pela sua senha
DB_HOST = 'dbintellimetrics.c3kc6gou2fhz.us-west-2.rds.amazonaws.com'  # ou o IP do seu servidor MySQL
DB_PORT = '3306'  # Porta padrão do MySQL
DB_NAME = 'DbIntelliMetrics'  # Nome do seu banco de dados
TABLE_NAME = 'TbDadosPlanilha'  # Nome da tabela

banco_url = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

app = Flask(__name__)
app.secret_key = '5160e59712d22d50e708220336549982'  # Necessário para usar sessões
app.config['SECRET_KEY'] = '5160e59712d22d50e708220336549982'

users = {
    "Luiz": "0312@2024", "usuario": "senha123", "rodrigo@taxidigital.net": "101275", "yham.miranda@predilarsolucoes.com.br": "1608@2024", "isabel@predilarsolucoes.com.br": "1608@2024", "maria.silva@predilarsolucoes.com.br": "2308@2024", "alex.acoroni@predilarsolucoes.com.br": "0410@2024"
}

UPLOAD_FOLDER = './uploads' # Create this folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['UPLOAD_FOLDER'] = './uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])



@app.route('/')
def home():
    return render_template('login.html')

@app.route('/api/ocr', methods=['POST'])
def ocr():
    #credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    #if not credentials_path:
        #return "Google credentials not set.", 500
    # Carrega as credenciais a partir da variável de ambiente
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

    # Crie um arquivo temporário para usar as credenciais
    if credentials_json:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(credentials_json.encode('utf-8'))
            temp_file_path = temp_file.name
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path

    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400

    # Converte a imagem em bytes e processa com o Google Cloud Vision
    client = vision.ImageAnnotatorClient()
    content = file.read()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        return jsonify({"error": response.error.message}), 500

    # Retorna o texto detectado, substituindo quebras de linha por espaço
    texto_extraido = texts[0].description.replace('\n', ' ') if texts else "Nenhum texto detectado."
    texto_extraido = texto_extraido.replace('\n', ' ')
    # Converter o texto em um dicionário JSON
    resultado_json = {}
    for linha in texto_extraido.splitlines():
        # Dividir a linha em chave e valor ao encontrar ':'
        if ':' in linha:
            chave, valor = linha.split(':', 1)
            resultado_json[chave.strip()] = valor.strip()  # Adiciona ao dicionário e limpa espaços

    # Imprimir o dicionário no terminal
    novo = (separar_campo(texto_extraido))
    print(novo)
    print("API OCR")
    return jsonify(resultado_json)
@app.route('/logip')
def logip():
    #return render_template( content=render_template('log_ip.html'))
    return render_template('log_ip.html')


@app.route('/delete_all_records', methods=['POST'])
def delete_all_records():
    conexao = conecta_bd()
    cursor = conexao.cursor()
            # Deletar todos os registros da tabela
    cursor.execute("DELETE FROM TbDadosPlanilha")
    conexao.commit()  # Confirma a transação
    return jsonify({"message": "Todos os registros foram excluídos com sucesso."}), 200


@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    print("toaqui")
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado', 400

    file = request.files['file']

    if file.filename == '':
        return 'Arquivo não selecionado', 400

    try:
        # Lê a planilha do Excel
        df = pd.read_excel(file)



        # Adiciona uma nova coluna com o nome da planilha
        nome_planilha = file.filename
        df['Nome da Planilha'] = nome_planilha

        # Rename columns based on COLUMN_MAPPING
        df.rename(columns=COLUMN_MAPPING, inplace=True)

        # Converte o DataFrame para um dicionário
        data_dict = df.to_dict(orient='records')



        # Conectar ao banco de dados e gravar dados
        gravar_dados_no_banco(df)
        return redirect(url_for('dados'))
        #return {'data': data_dict}, 200
    except Exception as e:
        return str(e), 400


@app.route('/log_ip')
def Seleciona_Log_IP():
    conexao = conecta_bd()  # Conecte ao banco de dados
    cursor = conexao.cursor(dictionary=True)
    comando = f"SELECT dsIp, MAX(dtRegistro) AS dtRegistro FROM  DbIntelliMetrics.TbAcessoIntelBras GROUP BY dsIp order by dtRegistro desc;"
    print(comando)
    cursor.execute(comando)
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(resultado)




@app.route('/dashboard')
def dashboard():
    username = username  # Função fictícia para obter o usuário atual
    print(username)
    return render_template('navbar.html', username=username)  # Substitua 'template.html' pelo seu nome de arquivo

@app.route('/teste')
def teste():
    return render_template('teste.html')


@app.route('/upload_file_plan', methods=['GET', 'POST'])
def upload_file_plan():
    dados = None

    if request.method == 'POST':
        file = request.files['file']

        if file and file.filename.endswith('.xlsx'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Processa o arquivo Excel
            df = pd.read_excel(file_path)
            dados = df.to_dict(orient='records')  # Transformar em lista de dicionários
            print(dados)
            # Remove o arquivo após processamento, se desejado
            os.remove(file_path)

    return render_template('upload.html', dados=dados)




#upload planilha transporte
@app.route('/upload_planilha', methods=['POST'])
def upload_planilha():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado', 400

    file = request.files['file']

    if file.filename == '':
        return 'Arquivo não selecionado', 400

    try:
        # Lê a planilha do Excel
        df = pd.read_excel(file)


        # Adiciona uma nova coluna com o nome da planilha
        nome_planilha = file.filename
        df['Nome da Planilha'] = nome_planilha

        # Rename columns based on COLUMN_MAPPING
        df.rename(columns=COLUMN_MAPPING, inplace=True)

        # Converte o DataFrame para um dicionário
        data_dict = df.to_dict(orient='records')


        # Conectar ao banco de dados e gravar dados
        gravar_dados_no_banco(df)
        return redirect(url_for('dados'))
        #return {'data': data_dict}, 200
    except Exception as e:
        return str(e), 400



@app.route('/cubagemold', methods=['GET'])
def cubagemold():
    # Capturar os parâmetros da query string
    Etiqueta = request.args.get('Etiqueta')
    nPeso = request.args.get('nPeso')
    nAlt = request.args.get('nAlt')
    nLarg = request.args.get('nLarg')
    nComp = request.args.get('nComp')
    token = request.args.get('token')

    # Validar se todos os parâmetros necessários estão presentes
    if not all([Etiqueta, nPeso, nAlt, nLarg, nComp, token]):
        print('Erro ao obter')
        return jsonify({"error": "Todos os parâmetros devem ser fornecidos."}), 400

    # Montar o dicionário com os dados
    dados_cubagem = {
        "Etiqueta": Etiqueta,
        "nPeso": float(nPeso),  # Convertendo para float
        "nAlt": float(nAlt),    # Convertendo para float
        "nLarg": float(nLarg),  # Convertendo para float
        "nComp": float(nComp)   # Convertendo para float
    }

    Update_TbDadosPlanilha(dados_cubagem)
    # Retornar o dicionário como resposta JSON
    return jsonify(dados_cubagem), 200


@app.route('/cubagem', methods=['GET','POST'])
def cubagem():
    # Capturar os parâmetros da query string
    xEtiqueta = request.args.get('xEtiqueta')
    nPeso = request.args.get('nPeso')
    nAlt = request.args.get('nAlt')
    nLarg = request.args.get('nLarg')
    nComp = request.args.get('nComp')
    nQtd = request.args.get('nQtd')
    token = request.args.get('token')

    Inserir_TbLog("TbDadosPlanilha", "Get_Cubagem", xEtiqueta, xEtiqueta)

    # Validar se todos os parâmetros necessários estão presentes
    #if not all([xEtiqueta, nPeso, nAlt, nLarg, nComp, token]):

     #   return jsonify({"error": "Todos os parâmetros devem ser fornecidos."}), 400

    # Tratar caso xEtiqueta ou nQtd sejam vazios
    xEtiqueta = xEtiqueta if xEtiqueta else 0
    nQtd = float(nQtd) if nQtd else 0.0

    # Montar o dicionário com os dados
    dados_cubagem = {
        "xEtiqueta": xEtiqueta,
        "nPeso": float(nPeso),  # Convertendo para float
        "nAlt": float(nAlt),    # Convertendo para float
        "nLarg": float(nLarg),  # Convertendo para float
        "nComp": float(nComp),   # Convertendo para float
        "nQtd": nQtd             # nQtd já é um float ou 0.0
    }
    print(dados_cubagem)

    Update_TbDadosPlanilha(dados_cubagem)
    # Retornar o dicionário como resposta JSON
    return jsonify(dados_cubagem), 200

@app.route('/get_zpl', methods=['POST'])
def get_zpl():
    # Gerar comando ZPL
    texto = request.json.get('texto', 'Texto padrão')
    zpl = f"""
    ^XA
    ^FO50,50^ADN,36,20^FD{texto}^FS
    ^XZ
    """
    return jsonify({ 'zpl': zpl })



@app.route('/enviawhats', methods=['POST'])
def enviawhats():
    data = request.get_json()
    dsCpf = data.get('cpf')
    #dsCelular = str(55) & data.get('celular')
    dsCelular = '55' + str(data.get('celular', ''))
    print(dsCelular)
    # Lógica para enviar QR via WhatsApp
    # Suponhamos que a função abaixo faz isso:
    try:
        print(dsCpf)
        cria_qr(dsCpf)
        ArquivoBase64 = cria_base64("QrCode.png")
        EnviaImgWhats(ArquivoBase64, dsCelular)
        print(ArquivoBase64)
        return jsonify(success=True)
    except Exception as e:
        print(f"Erro ao enviar QR: {e}")
        return jsonify(success=False), 500





@app.route('/login', methods=['POST'])
def login():
    global login_usuario
    global dsIp
    dsIp = obter_ip_publico()
    username = request.form['username']
    password = request.form['password']
    login_usuario =  username  # Armazena o valor na sessão

    if username in users and users[username] == password:
        Inserir_TbLog("TbLogin", "ACESSO PERMITIDO", dsIp, login_usuario)
        if username != "Luiz":

            return render_template('home.html',username=username)
        else:
            if password != "0312@2024":
                return render_template('upload.html', username=username)
            else:
                return render_template('capturar.html', username=username)
    else:
        Inserir_TbLog("TbLogin", "ACESSO INVÁLIDO", dsIp, login_usuario)
        return render_template('login.html', message='Usuário ou senha inválidos!')



@app.route('/usuarios')
def usuarios():
    Usuarios = (pesquisa_usuarios())
    Inserir_TbLog("TbUsuarios", "Usuarios", dsIp, login_usuario)
    return render_template("usuarios.html", usuarios=Usuarios)

@app.route('/cadastro_horas')
def cadastro_horas():
   # Usuarios = (pesquisa_usuarios())
    #Inserir_TbLog("TbUsuarios", "Usuarios", dsIp, login_usuario)
    return render_template("cadastro_horas.html")




@app.route('/cadastro_clientes', methods=['GET', 'POST'])
def cadastro_clientes():
    form_cliente = FormCliente()
    Clientes = (pesquisa_clientes())
    Inserir_TbLog("TbClientes", "Cadastro de Clientes", dsIp, login_usuario)


    if form_cliente.validate_on_submit() and 'botao_submit_cadastrar' in request.form:
        flash(f'Cliente adicionado {form_cliente.dsNome.data}', 'alert-success')
        return redirect(url_for('cadastro_clientes'))
    return render_template("cadastro_clientes.html", form_cliente=form_cliente, clientes=Clientes)

@app.route('/cadastro_destinatarios', methods=['GET', 'POST'])
def cadastro_destinatarios():
    form_destinatario = FormDestinatario()
    Destinatarios= pesquisa_destinatarios()
    Inserir_TbLog("TbDestinatarios", "Cadastro Posto de Trabalho", dsIp, login_usuario)


    if form_destinatario.validate_on_submit() and 'botao_submit_cadastrar' in request.form:
        flash(f'Destinatario adicionado {form_destinatario.dsNome.data}', 'alert-success')
        return redirect(url_for('cadastro_destinatarios'))
    return render_template("cadastro_destinatarios.html", form_destinatario=form_destinatario, destinatarios=Destinatarios)


@app.route('/cadastro_funcionarios', methods=['GET', 'POST'])
def cadastro_funcionarios():
    form_funcionario = FuncionarioForm()
    funcionarios = pesquisa_funcionarios()
    Inserir_TbLog("TbCadastroFuncionrios", "Cadastro de Funcionários ", dsIp, login_usuario)
    print(funcionarios)

    if request.method == 'POST':
        i = 1
        if i == 1:

        #if form_funcionario.botao_submit_cadastrar():  # Validando se o formulário foi preenchido corretamente
            # Aqui você pegaria os dados do formulário
            print("func-ok")
            nrCodEmpregado = form_funcionario.cdFuncionario.data
            dsNomeEmpregado = form_funcionario.dsNomeEmpregado.data
            dsCpf = form_funcionario.dsCpf.data
            dsEmail = form_funcionario.dsEmail.data
            dsCelular = form_funcionario.dsCelular.data
            dsEntrada = form_funcionario.dsEntrada.data
            dsSaida = form_funcionario.dsSaida.data
            cdPerfil = form_funcionario.cdPerfil.data
            dsFuncao = form_funcionario.dsFuncao.data
            dsEmpresa = form_funcionario.dsEmpresa.data
            dsEscala = form_funcionario.dsEscala.data
            nrCargaHoraria = form_funcionario.nrCargaHoraria.data
            nrCargaHorariaMes = form_funcionario.nrCargaHorariaMes.data
            if 'botao_submit_cadastrar' in request.form:
                Inserir_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsCpf, dsEmail, dsCelular, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes)
                print(nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida)
                #return redirect(url_for('cadastro_funcionarios'))  # Redireciona para a própria página ou outra após o cadastro
                flash(f'Funcionario adicionado {form_funcionario.dsNomeEmpregado.data}', 'alert-success')
            if 'botao_submit_alterar' in request.form:
                print(nrCodEmpregado, dsNomeEmpregado)
                cria_qr(dsCpf)
                Alterar_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsCpf, dsEmail, dsCelular, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa,  dsEscala, nrCargaHoraria, nrCargaHorariaMes)
            if 'botao_submit_excluir' in request.form:
                print(nrCodEmpregado, dsNomeEmpregado)
                Excluir_TbFuncionario(dsCpf)

                # return redirect(url_for('cadastro_funcionarios'))  # Redireciona para a própria página ou outra após o cadastro
                flash(f'Funcionario Excluido {form_funcionario.dsNomeEmpregado.data}', 'alert-success')

            return redirect(url_for('cadastro_funcionarios'))

    return render_template('cadastro_funcionarios.html', form_funcionario=form_funcionario, funcionarios=funcionarios)






@app.route('/cadastro_usuarios', methods=['GET', 'POST'])
def cadastro_usuarios():
    form_usuario = FormUsuario()
    Usuarios = (pesquisa_usuarios())
    Inserir_TbLog("TbCadastroUsuarios", " Cadastro de Usuarios", dsIp, login_usuario)

    if form_usuario.validate_on_submit() and 'botao_submit_cadastrar' in request.form:
        flash(f'Usuario adicionado {form_usuario.dsNome.data}', 'alert-success')
        return redirect(url_for('cadastro_usuarios'))
    return render_template("cadastro_usuarios.html", form_usuario=form_usuario, Usuarios=Usuarios)

@app.route('/rel_ponto')
def rel_ponto():
    Inserir_TbLog("TbPonto", "Relatório de Ponto", dsIp, login_usuario)
    return render_template("rel_ponto.html")


def converter_hora(hora):


    if hora == "":
        return "00:00"  # Retorna 00:00 se a hora for null
    return hora  # Se não for null, retorna a hora original

def comparar_listas(dicionario_a, dicionario_b):
    dicionario_diferencas = []

    # Convertendo a lista de dicionários em um dicionário para acesso mais rápido
    dict_a = {item['cdPonto']: item for item in dicionario_a}
    dict_b = {item['cdPonto']: item for item in dicionario_b}

    # Comparar os dicionários das duas listas
    for cdPonto in dict_a:
        if cdPonto in dict_b:
            if dict_a[cdPonto]['dsRegistro01'] != dict_b[cdPonto]['dsRegistro01'] or dict_a[cdPonto]['dsRegistro02'] != dict_b[cdPonto]['dsRegistro02'] or dict_a[cdPonto]['dsRegistro03'] != dict_b[cdPonto]['dsRegistro03'] or dict_a[cdPonto]['dsRegistro04'] != dict_b[cdPonto]['dsRegistro04'] or dict_a[cdPonto]['dsTipoRegistro'] != dict_b[cdPonto]['dsTipoRegistro'] or dict_a[cdPonto]['dsObservacao'] != dict_b[cdPonto]['dsObservacao']:
                dicionario_diferencas.append({
                    'cdPonto': cdPonto,
                    'dsRegistro01_A': dict_a[cdPonto]['dsRegistro01'],
                    'dsRegistro01_B': dict_b[cdPonto]['dsRegistro01'],
                    'dsRegistro02_A': dict_a[cdPonto]['dsRegistro02'],
                    'dsRegistro02_B': dict_b[cdPonto]['dsRegistro02'],
                    'dsRegistro03_A': dict_a[cdPonto]['dsRegistro03'],
                    'dsRegistro03_B': dict_b[cdPonto]['dsRegistro03'],
                    'dsRegistro04_A': dict_a[cdPonto]['dsRegistro04'],
                    'dsRegistro04_B': dict_b[cdPonto]['dsRegistro04'],
                    'dsData': dict_b[cdPonto]['dsData'],
                    'dsTipoRegistro_A': dict_a[cdPonto]['dsTipoRegistro'],
                    'dsTipoRegistro_B': dict_b[cdPonto]['dsTipoRegistro'],
                    'dsObservacao_A': dict_a[cdPonto]['dsObservacao'],
                    'dsObservacao_B': dict_b[cdPonto]['dsObservacao']
                })

    # Verificar se há registros em dict_b que não estão em dict_a
    for cdPonto in dict_b:
        if cdPonto not in dict_a:
            dicionario_diferencas.append({
                'cdPonto': cdPonto,
                'dsRegistro01_A': None,  # Não existe em dicionario_a
                'dsRegistro01_B': dict_b[cdPonto]['dsRegistro01'],

                'dsRegistro02_A': None,  # Não existe em dicionario_a
                'dsRegistro02_B': dict_b[cdPonto]['dsRegistro02'],

                'dsRegistro03_A': None,  # Não existe em dicionario_a
                'dsRegistro03_B': dict_b[cdPonto]['dsRegistro03'],

                'dsRegistro04_A': None,  # Não existe em dicionario_a
                'dsRegistro04_B': dict_b[cdPonto]['dsRegistro04'],

                'dsData': dict_b[cdPonto]['dsData'],
                'dsTipoRegistro': dict_b[cdPonto]['dsTipoRegistro'],
                'dsObservacao': dict_b[cdPonto]['dsObservacao']
            })

    return dicionario_diferencas


@app.route('/dados')
def dados():
    return render_template('dados.html')



@app.route('/get_dados', methods=['GET'])
def mostrar_dados():
    print("chamou")
    try:
        get_dados = pesquisa_planilha()
        print(get_dados)

        return jsonify(get_dados)
    except Exception as e:
        return str(e), 400




@app.route('/data', methods=['GET', 'POST', 'PUT'])
def data():
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
  #  start_date = request.args.get('start', '')
  #  end_date = request.args.get('end', '')
  #  funcionario = request.args.get('employee', '')
  #  print(funcionario)
    today = datetime.today().strftime('%Y-%m-%d')
    start_date = request.args.get('start', today)
    end_date = request.args.get('end', today)
    funcionario = request.args.get('employee', '')



    query = """
        SELECT 
            cdPonto, 
            TRIM(dsCardName) AS dsCardName,
            dsCardNo, 
            DATE_FORMAT(STR_TO_DATE(dsRegistroAut, '%Y-%m-%d %H:%i:%s'), '%d/%m/%Y') AS dsData,
            DATE_FORMAT(STR_TO_DATE(dsRegistro01, '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d %H:%i') AS dsRegistro00,
            DATE_FORMAT(STR_TO_DATE(dsRegistro01, '%Y-%m-%d %H:%i:%s'), '%H:%i') AS dsRegistro01,
            DATE_FORMAT(STR_TO_DATE(dsRegistro02, '%Y-%m-%d %H:%i:%s'), '%H:%i') AS dsRegistro02,
            DATE_FORMAT(STR_TO_DATE(dsRegistro03, '%Y-%m-%d %H:%i:%s'), '%H:%i') AS dsRegistro03,
            DATE_FORMAT(STR_TO_DATE(dsRegistro04, '%Y-%m-%d %H:%i:%s'), '%H:%i') AS dsRegistro04,
            dsTipoRegistro,
            dsObservacao
        FROM
            DbIntelliMetrics.TbPonto 
    """
 #   print(query)
 #   print('incio')
 #   print(start_date)
 #   print(end_date)
    if start_date != '' and end_date != '' or funcionario != '':
        query += " WHERE dsRegistroAut >='" + start_date + "' AND dsRegistroAut <='" + end_date + "' and dsCardname like'%" + funcionario + "%' order by dsRegistroAut"
        #params = (start_date, end_date)
        cursor.execute(query)
      #  print('oi')
      #  print(query)
    else:
        query += "  order by dsRegistroAut"

        cursor.execute(query)
      #  print('oi2')

    result = cursor.fetchall()
    #return jsonify(result)


    #dicionario = ponto()
    dicionario = Selecionar_TbPonto()
    #print(dicionario)

    dic01 = []
    for dic1 in dicionario:
       #dic01.append ({'cdPonto': dic1['cdPonto'], 'dsRegistro01': dic1['dsRegistro01'], 'dsRegistro02': dic1['dsRegistro02'], 'dsRegistro03': dic1['dsRegistro03'], 'dsRegistro04': dic1['dsRegistro04'], 'dsTipoRegistro': dic1['dsTipoRegistro'], 'dsObservacao': dic1['dsObservacao']})
       def replace_nome_with_empty(value):
           """Replace 'Nome' with an empty string in a given value."""
           return '' if value == None else value

       # Assume dic01 and dic1 are defined
       dic01.append({
           'cdPonto': replace_nome_with_empty(dic1.get('cdPonto')),
           'dsRegistro01': replace_nome_with_empty(dic1.get('dsRegistro01')),
           'dsRegistro02': replace_nome_with_empty(dic1.get('dsRegistro02')),
           'dsRegistro03': replace_nome_with_empty(dic1.get('dsRegistro03')),
           'dsRegistro04': replace_nome_with_empty(dic1.get('dsRegistro04')),
           'dsTipoRegistro': replace_nome_with_empty(dic1.get('dsTipoRegistro')),
           'dsObservacao': replace_nome_with_empty(dic1.get('dsObservacao'))
       })

   # print(dic01)

     #return jsonify(result)

    if request.method == 'POST':

        dados = request.get_json()
        payload = json.dumps(dados)

        #comparar_dicionarios(dicionario, dados)
       # print("-----------------------------------------------------------------")
        #print(dados)

        dic02 = []
        Horas_Array = []
        for dado in dados:
            #dic02.append({'cdPonto': dado['cdPonto'], 'dsRegistro01': dado['dsRegistro01'], 'dsRegistro02': dado['dsRegistro02'], 'dsRegistro03': dado['dsRegistro03'], 'dsRegistro04': dado['dsRegistro04'], 'dsData': dado['dsData'], 'dsTipoRegistro': dado['dsTipoRegistro'], 'dsObservacao': dado['dsObservacao']})
            dic02.append({
                'cdPonto': dado.get('cdPonto'),
                'dsRegistro01': dado.get('dsRegistro01'),
                'dsRegistro02': dado.get('dsRegistro02'),
                'dsRegistro03': dado.get('dsRegistro03'),
                'dsRegistro04': dado.get('dsRegistro04'),
                'dsData': dado.get('dsData'),
                'dsTipoRegistro': dado.get('dsTipoRegistro'),
                'dsObservacao': dado.get('dsObservacao')
            })

            cdPonto = dado['cdPonto']
            dsRegistro01 = dado['dsRegistro01']
            dsRegistro02 = dado['dsRegistro02']
            dsRegistro03 = dado['dsRegistro03']
            dsRegistro04 = dado['dsRegistro04']
            dsData = dado['dsData']
            dsTipoRegistro = dado['dsTipoRegistro']
            dsObservacao = dado['dsObservacao']
            #Alterar_TbPonto(cdPonto, dsRegistro01)
       # print(dic02)

        # Comparar os dicionários
        diferencas = comparar_listas(dic01, dic02)

        # Exibir as diferenças

        for item in diferencas:
            #print(item)
           # print(item['cdPonto'])
           # print(item['dsRegistro01_B'])
            Alterar_TbPonto(item['cdPonto'], item['dsRegistro01_B'], item['dsRegistro02_B'], item['dsRegistro03_B'], item['dsRegistro04_B'], item['dsData'],item['dsTipoRegistro_B'],item['dsObservacao_B'])

    return jsonify(result)


@app.route('/data2')
def data2():
    return get_today_data()

@app.route('/planilha', methods=['GET','POST'])
def planilha():
    if request.method == 'POST':
        data1 = request.get_json()
        texto = data1.get('mensagem')
        update_st_impresso(data1)

    return pesquisa_planilha()




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

#VAMOS AJUSTAR A CAPTURA E TELA

@app.route('/captura')
def captura():
    return render_template('capturar.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/api/get-origem')
def get_origem():
    return jsonify(vresultado_origem)

@app.route('/api/get-origem_reload', methods=['POST'])
def get_origem_reload():
    data = request.get_json()  # Obtém os dados da requisição JSON
    origem = data.get('origem')  # Pega o valor da origem
    latitudeUF, longitudeUF = get_uf(origem)
    print(data)
    print("data")
    print(origem)
    print("origem")
    print(latitudeUF)
    print(longitudeUF)

    coordenada_origem = (consulta_get_places(latitudeUF, longitudeUF, raio, origem))
    print(coordenada_origem)
    print("coordenada_origem1612")
    return jsonify(vresultado_origem)




@app.route('/api/dados_geral')
def get_dados_geral():
    return jsonify(vresultado_dados_geral)



@app.route('/api/get-destino')
def get_destino():
    return jsonify(vresultado_destino)
@medir_tempo_execucao
@app.route('/api/gerar_chamado', methods=['POST'])
def gerar_chamado():
    dados = request.get_json()  # Obtém os dados da requisição JSON
    print(dados)
    print("dados_gerar")
    # Valida se todos os campos necessários estão presentes
   # required_fields = ['voucher', 'observacao', 'telefone', 'origem', 'destino', 'valor', 'viajantes', 'datas', 'hora', 'inputLatOrigem', 'inputLongOrigem', 'inputLatDestino', 'inputLongDestino']
   # for field in required_fields:
   #     if field not in dados or not dados[field]:
   #         return jsonify({'error': f'Campo {field} é obrigatório.'}), 400

    voucher = dados['voucher']
    observacao = dados['observacao']
    viajantes = dados['viajantes']
    origem = dados['origem']
    destino = dados['destino']
    valor = dados['valor']
    data = dados['datas']
    hora = dados['hora']
    inputLatOrigem = dados['inputLatOrigem']
    inputLongOrigem = dados['inputLongOrigem']
    inputLatDestino = dados['inputLatDestino']
    inputLongDestino = dados['inputLongDestino']
    telefone = dados['telefone']
    wpet = gerachamado( voucher, observacao, viajantes, telefone, origem, destino, valor, hora, data, inputLatOrigem, inputLongOrigem, inputLatDestino, inputLongDestino)
    #dsAcao = wpet
    Inserir_TbLog("API", wpet, dsIp, login_usuario)
    print("wpet")
    #print(wpet)
    return jsonify({'message': 'Chamado gerado com sucesso!'}, wpet), 200


@app.route('/api/capture-image', methods=['POST'])
def capture_image():
    print("aqui00")
    if request.method == 'POST':
        print("aqui01")
        try:
            # Verifica se um arquivo foi enviado
            if 'file' not in request.files:
                return jsonify({"error": "Nenhum arquivo enviado."}), 400

            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "Nenhum arquivo selecionado."}), 400

            # Carrega a imagem
            imagem = Image.open(io.BytesIO(file.read()))
            print("aqui02")

            # Caminho onde a imagem será salva
            image_dir = 'imagens'
            os.makedirs(image_dir, exist_ok=True)  # Cria o diretório se não existir
            image_path = os.path.join(image_dir, 'voucher.jpeg')
            print("aqui03")

            # Salva a imagem
            imagem.save(image_path)
            print(f"Imagem capturada e salva em: {image_path}")

            # Chame a função OCR para processar a imagem (substitua pelo seu código de OCR)
            texto = ocr()
            print(texto)
            dados_viagem = separar_campo(texto)

            return jsonify({"message": dados_viagem})


        except Exception as e:
            return jsonify({"error": "Ocorreu um erro ao processar a imagem: " + str(e)}), 500
    return (vresultado_origem)



if __name__ == '__main__':
    app.run(debug=True)



#def main():
#    port = int(os.environ.get("PORT", 80))
#    app.run(host="192.168.0.113", port=port)



#if __name__ == "__main__":
#    main()



