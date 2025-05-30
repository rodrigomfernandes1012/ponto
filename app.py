# app.py
from flask import Flask, render_template, request, jsonify
import boto3
import base64
import os

app = Flask(__name__)

# Carrega as credenciais AWS do ambiente
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.environ.get('REGION_NAME', 'us-east-1')  # Valor padrão se não estiver definido

# Verifica se as credenciais foram definidas
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise ValueError("As variáveis de ambiente AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY devem ser definidas.")

# Inicializa o cliente Rekognition fora da rota
client = boto3.client('rekognition',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=REGION_NAME)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    data = request.json['image']
    # Remove o prefix 'data:image/jpeg;base64,'
    encoded_data = data.split(',')[1]
    img_bytes = base64.b64decode(encoded_data)

    # Envia a imagem ao Rekognition
    try:
        response = client.detect_faces(
            Image={'Bytes': img_bytes},
            Attributes=['ALL']
        )
        faces = response['FaceDetails']
    except Exception as e:
        print(f"Erro ao chamar o Rekognition: {e}")
        return jsonify({'error': str(e)}), 500  # Retorna um erro 500

    resultados = []
    for face in faces:
        face_info = {
            'BoundingBox': face['BoundingBox'],
            'Confidence': face['Confidence'],
            'AgeRange': face['AgeRange'],
            'Emotions': face['Emotions'],
            'Gender': face['Gender'],
            'Smile': face.get('Smile', {}),
            'FacialHair': face.get('FacialHair', {}),
            'EyesOpen': face.get('EyesOpen', {}),
            'MouthOpen': face.get('MouthOpen', {})
        }
        resultados.append(face_info)

    return jsonify({'faces': resultados})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)), debug=True) # Heroku utiliza variável de ambiente PORT