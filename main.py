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




def ponto():
    url = "https://replit.taxidigital.net/Ponto"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    selecao = json.loads(response.text)

    dados_dicionario = {}

    for registro in selecao:
        nome = registro['dsCardName']
        dados_dicionario[nome] = []
        dados_dicionario[nome] = [data]
        dados_dicionario[nome].append(data)
        return selecao

def get_ponto():
  conexao = conecta_bd()
  cursor = conexao.cursor(dictionary=True)
  comando = f'SELECT * FROM DbIntelliMetrics.TbAcessoIntelBras where dsStatus = 1 and dsUtc >= 1722502193 ;'
  cursor.execute(comando)
  selecao = cursor.fetchall() # ler o banco de dados
  dados_dicionario = {}

  for registro in selecao:
      nome = registro['dsCardName']

      datacompleta = int(registro['dsUtc'])
      data = (datetime.utcfromtimestamp(datacompleta).strftime('%d-%m-%Y'))
      dados_dicionario[nome] = []
      dados_dicionario[nome] = [data]
      dados_dicionario[nome].append(data)
  cursor.close()
  conexao.close()
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

    for funcionario in funcionarios:
        (
            dsCardNo,
        ) = funcionario
        dsCardNo = (funcionario['dsCardNo'])
        funcionarios_json.append(funcionario)
        conexao = conecta_bd()
        cursor = conexao.cursor(dictionary=True)
        comando = f'SELECT dsUtc FROM DbIntelliMetrics.TbAcessoIntelBras where dsStatus = 1 and dsutc >=1722506000  and dsCardNo = {dsCardNo};'
        cursor.execute(comando)
        datas = cursor.fetchall()
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


def format_timedelta(td):
    """Format a timedelta object into a string of hours and minutes (HH:mm)."""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)  # 3600 seconds in an hour
    minutes = remainder // 60  # Get the minutes from the remainder
    return f"{hours:02}:{minutes:02}"  # Format as HH:mm

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
    return render_template('login.html', message='')

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


@app.route('/data', methods=['GET', 'POST', 'PUT'])
def data():
    dicionario = ponto()
    people = dicionario

    url = "https://replit.taxidigital.net/AlteraPonto"

    if request.method == 'POST':

        dados = request.get_json()
        payload = json.dumps(dados)
        #print(dados)


        Horas_Array = []
        for dado in dados:
            dsRegistro01 = dado
            #data = str(dado['dsData'] +' ' + dado['dsRegistro01'])
            dsData01 = dado['dsRegistro01']
            #dsData02 = dado['dsData'] + ' ' + converter_hora(dado['dsRegistro02'])
            #dsRegistro01 = dict(datetime.strptime(dsData01, "%d/%m/%Y %H:%M"))
            #dsRegistro02 = datetime.strptime(dsData02, "%d/%m/%Y %H:%M")
            #dsRegistro02 = datetime.strptime((dado['dsData'] + ' ' + dado['dsRegistro02']), "%d/%m/%Y %H:%M")
            #dsRegistro03 = datetime.strptime((dado['dsData'] + ' ' + dado['dsRegistro03']), "%d/%m/%Y %H:%M")
            #dsRegistro04 = datetime.strptime((dado['dsData'] + ' ' + dado['dsRegistro04']), "%d/%m/%Y %H:%M")
            #print({"dsRegistro01": dsRegistro01})
            #print(data2)

            #ponto_json = {"cdPonto": cdPonto,}
            Horas_Array.append({"cdPonto": dado['cdPonto']},)
            Horas_Array.append({"dsRegistro01": dado['dsRegistro01']})
            #print(Horas_Array)

            Horas_Array = []




        headers = 'Content-Type : application/json'


    return jsonify(people)



def main():
    port = int(os.environ.get("PORT", 80))
    app.run(host="192.168.15.200", port=port)


if __name__ == "__main__":
    main()



