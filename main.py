from flask import Flask, jsonify,  render_template,  request, redirect, flash,  url_for
import mysql.connector
from forms import    FormCliente, FormDestinatario, FormUsuario, FuncionarioForm
import os
import requests
from datetime import datetime
import json
import qrcode


token = "8c4EF9vXi8TZe6581e0af85c25"

def conecta_bd():
  conexao = mysql.connector.connect(
  host='dbintellimetrics.c3kc6gou2fhz.us-west-2.rds.amazonaws.com',
  user='admin',
  password='IntelliMetr!c$',
  database='DbIntelliMetrics')
  return conexao

def Selecionar_TbPonto():
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
    comando = f"select cdPonto,  TRIM(dsCardName) as dsCardName,  DATE_FORMAT(STR_TO_DATE(dsRegistro01, '%Y-%m-%d %H:%i:%s'), '%d/%m/%Y') AS dsData, DATE_FORMAT(STR_TO_DATE(dsRegistro01, '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d %H:%i') AS dsRegistro00,  DATE_FORMAT(STR_TO_DATE(dsRegistro01, '%Y-%m-%d %H:%i:%s'), '%H:%i') AS dsRegistro01, dsTipoRegistro, dsObservacao  from DbIntelliMetrics.TbPonto where dsTipoRegistro <> 'Remover' order by dsCardName asc, dsRegistro00 asc ;"
    print(comando)
    cursor.execute(comando)
    resultado = cursor.fetchall()
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
def Alterar_TbPonto(cdPonto, dsRegistro01,dsData, dsTipoRegistro, dsObservacao ):
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
    comando = f"update DbIntelliMetrics.TbPonto set dsRegistro01 = STR_TO_DATE('{dsData} {dsRegistro01}', '%d/%m/%Y %H:%i'), dsTipoRegistro = '{dsTipoRegistro}', dsObservacao = '{dsObservacao}' where cdPonto = '{cdPonto}'"
    print(comando)
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()


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
  comando = f'SELECT nrCodEmpregado as cdFuncionario, dsNomeEmpregado, dsCpf, dsEntrada, dsSaida, dsFuncao, dsEmpresa,   dsEscala, nrCargaHoraria, nrCargaHorariaMes, cdPerfil FROM DbIntelliMetrics.TbFuncionario;'
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

def Inserir_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes):
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
    comando = f'insert into DbIntelliMetrics.TbFuncionario (nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes) values ("{nrCodEmpregado}", "{dsNomeEmpregado}", "{dsEntrada}", "{dsSaida}", "{cdPerfil}", "{dsFuncao}", "{dsEmpresa}", "{dsEscala}", "{nrCargaHoraria}", "{nrCargaHorariaMes}")'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

def Alterar_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsCpf, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes):
    conexao = conecta_bd()
    cursor = conexao.cursor()
    comando = f"update  DbIntelliMetrics.TbFuncionario set dsNomeEmpregado = '{dsNomeEmpregado}', dsCpf = '{dsCpf}', dsEntrada = '{dsEntrada}', dsSaida = '{dsSaida}', cdPerfil = '{cdPerfil}', dsFuncao = '{dsFuncao}', dsEmpresa = '{dsEmpresa}', dsEscala = '{dsEscala}', nrCargaHoraria = '{nrCargaHoraria}', nrCargaHorariaMes = '{nrCargaHorariaMes}' where nrCodEmpregado = '{nrCodEmpregado}'"
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
    conexao = conecta_bd()
    cursor = conexao.cursor(dictionary=True)
    comando = f'insert into DbIntelliMetrics.TbLog (dsTbAcesso, dsAcao, dsIp, dsLogin) values ("{dsTbAcesso}", "{dsAcao}", "{dsIp}", "{dsLogin}")'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()
    username = dsLogin
    return username

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

app = Flask(__name__)
app.secret_key = '5160e59712d22d50e708220336549982'  # Necessário para usar sessões
app.config['SECRET_KEY'] = '5160e59712d22d50e708220336549982'

users = {
    "usuario": "senha123", "rodrigo@taxidigital.net": "101275", "yham.miranda@predilarsolucoes.com.br": "1608@2024", "isabel@predilarsolucoes.com.br": "1608@2024", "maria.silva@predilarsolucoes.com.br": "2308@2024"
}

def cria_qr(dsCpf):
    print("qr")
    valor =str(dsCpf)
    vtipo = '.png'
    imagem = qrcode.make(valor)
    imagem.save(valor + vtipo)





login_usuario = None
dsIp = None
@app.route('/')
def home():
    return render_template('home.html', message='')

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
        return render_template('home.html')

    else:
        Inserir_TbLog("TbLogin", "ACESSO INVÁLIDO", dsIp, login_usuario)
        return render_template('login.html', message='Usuário ou senha inválidos!')



@app.route('/usuarios')
def usuarios():
    Usuarios = (pesquisa_usuarios())
    Inserir_TbLog("TbUsuarios", "Usuarios", dsIp, login_usuario)
    return render_template("usuarios.html", usuarios=Usuarios)

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
            dsEntrada = form_funcionario.dsEntrada.data
            dsSaida = form_funcionario.dsSaida.data
            cdPerfil = form_funcionario.cdPerfil.data
            dsFuncao = form_funcionario.dsFuncao.data
            dsEmpresa = form_funcionario.dsEmpresa.data
            dsEscala = form_funcionario.dsEscala.data
            nrCargaHoraria = form_funcionario.nrCargaHoraria.data
            nrCargaHorariaMes = form_funcionario.nrCargaHorariaMes.data
            if 'botao_submit_cadastrar' in request.form:
                Inserir_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsCpf, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa, dsEscala, nrCargaHoraria, nrCargaHorariaMes)
                print(nrCodEmpregado, dsNomeEmpregado, dsEntrada, dsSaida)
                #return redirect(url_for('cadastro_funcionarios'))  # Redireciona para a própria página ou outra após o cadastro
                flash(f'Funcionario adicionado {form_funcionario.dsNomeEmpregado.data}', 'alert-success')
            if 'botao_submit_alterar' in request.form:
                print(nrCodEmpregado, dsNomeEmpregado)
                cria_qr(dsCpf)
                Alterar_TbFuncionario(nrCodEmpregado, dsNomeEmpregado, dsCpf, dsEntrada, dsSaida, cdPerfil, dsFuncao, dsEmpresa,  dsEscala, nrCargaHoraria, nrCargaHorariaMes)
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
            if dict_a[cdPonto]['dsRegistro01'] != dict_b[cdPonto]['dsRegistro01'] or dict_a[cdPonto]['dsTipoRegistro'] != dict_b[cdPonto]['dsTipoRegistro'] or dict_a[cdPonto]['dsObservacao'] != dict_b[cdPonto]['dsObservacao']:
                dicionario_diferencas.append({
                    'cdPonto': cdPonto,
                    'dsRegistro01_A': dict_a[cdPonto]['dsRegistro01'],
                    'dsRegistro01_B': dict_b[cdPonto]['dsRegistro01'],
                    'dsData': dict_b[cdPonto]['dsData'],
                    'dsTipoRegistro': dict_b[cdPonto]['dsTipoRegistro'],
                    'dsObservacao': dict_b[cdPonto]['dsObservacao']
                })

    # Verificar se há registros em dict_b que não estão em dict_a
    for cdPonto in dict_b:
        if cdPonto not in dict_a:
            dicionario_diferencas.append({
                'cdPonto': cdPonto,
                'dsRegistro01_A': None,  # Não existe em dicionario_a
                'dsRegistro01_B': dict_b[cdPonto]['dsRegistro01'],
                'dsData': dict_b[cdPonto]['dsData'],
                'dsTipoRegistro': dict_b[cdPonto]['dsTipoRegistro'],
                'dsObservacao': dict_b[cdPonto]['dsObservacao']
            })

    return dicionario_diferencas







@app.route('/data', methods=['GET', 'POST', 'PUT'])
def data():
    #dicionario = ponto()
    dicionario = Selecionar_TbPonto()
    #print(dicionario)

    dic01 = []
    for dic1 in dicionario:
        dic01.append ({'cdPonto': dic1['cdPonto'], 'dsRegistro01': dic1['dsRegistro01'], 'dsTipoRegistro': dic1['dsTipoRegistro'], 'dsObservacao': dic1['dsObservacao']})

    #print(dic01)



    if request.method == 'POST':

        dados = request.get_json()
        payload = json.dumps(dados)

        #comparar_dicionarios(dicionario, dados)
        #print("-----------------------------------------------------------------")
        print(dados)

        dic02 = []
        Horas_Array = []
        for dado in dados:
            dic02.append({'cdPonto': dado['cdPonto'], 'dsRegistro01': dado['dsRegistro01'], 'dsData': dado['dsData'], 'dsTipoRegistro': dado['dsTipoRegistro'], 'dsObservacao': dado['dsObservacao']})
            cdPonto = dado['cdPonto']
            dsRegistro01 = dado['dsRegistro01']
            dsData = dado['dsData']
            dsTipoRegistro = dado['dsTipoRegistro']
            dsObservacao = dado['dsObservacao']
            #Alterar_TbPonto(cdPonto, dsRegistro01)
        print(dic02)

        # Comparar os dicionários
        diferencas = comparar_listas(dic01, dic02)

        # Exibir as diferenças
        print("Diferenças encontradas:")
        for item in diferencas:
            print(item)
            print(item['cdPonto'])
            print(item['dsRegistro01_B'])
            Alterar_TbPonto(item['cdPonto'], item['dsRegistro01_B'],item['dsData'],item['dsTipoRegistro'],item['dsObservacao'])

    return jsonify(dicionario)

    #print(dicionario_diferencas)



def main():
    port = int(os.environ.get("PORT", 8081))
    app.run(host="192.168.15.200", port=port)


if __name__ == "__main__":
    main()



