from flask import Flask, jsonify, render_template
#import random

app = Flask(__name__)

motor_status = 0  # Status inicial do motor (0 - desligado, 1 - ligado)

@app.route('/')
def home():
    return render_template('index.html')  # Renderiza a página HTML

@app.route('/motor', methods=['GET'])
def consultar_motor():
    return jsonify(motor_status)  # Retorna o status do motor como JSON

@app.route('/set_motor/<int:status>', methods=['POST'])
def set_motor(status):
    global motor_status
    motor_status = status
    return jsonify({"status": motor_status})  # Retorna o novo status como JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Executa o app na porta 5000