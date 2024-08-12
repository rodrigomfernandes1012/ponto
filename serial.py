import flask
import mysql.connector
import serial

app = flask.Flask(__name__)

# Configurações do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'seu_usuario'
app.config['MYSQL_PASSWORD'] = 'sua_senha'
app.config['MYSQL_DB'] = 'seu_banco_de_dados'

# Criação da instância do MySQL
#mysql = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="seu_banco_de_dados"
)

# Configuração da porta serial
ser = serial.Serial('COM6', 9600)  # Substitua 'COM1' pela porta serial correta


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        # Obter os dados do formulário
        codigo = flask.request.form['codigo']
        obs = flask.request.form['obs']
        altura = flask.request.form['altura']
        largura = flask.request.form['largura']
        comprimento = flask.request.form['comprimento']
        peso_real = flask.request.form['peso_real']
        peso_cubado = flask.request.form['peso_cubado']
        usuario = flask.request.form['usuario']

        # Inserir os dados no banco de dados
        #cursor = mysql.cursor()
        #sql = "INSERT INTO tabela (codigo, obs, altura, largura, comprimento, peso_real, peso_cubado, usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        #values = (codigo, obs, altura, largura, comprimento, peso_real, peso_cubado, usuario)
        #cursor.execute(sql, values)
        #mysql.commit()
        #cursor.close()

    # Ler a porta serial
    leitura_serial = ser.readline().decode().strip()

    return flask.render_template('pserial.html', leitura_serial=leitura_serial)


if __name__ == '__main__':
    app.run()
