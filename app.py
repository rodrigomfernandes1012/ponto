from flask import Flask, render_template, request, jsonify
import boto3
import base64
import os
from dotenv import load_dotenv

load_dotenv()
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

# --- Funções de Tradução ---

def traduzir_emocao(emocao_en):
    mapa_emocoes = {
        'HAPPY': 'FELIZ',
        'SAD': 'TRISTE',
        'ANGRY': 'ZANGADO',
        'CONFUSED': 'CONFUSO',
        'DISGUSTED': 'ENJOADO',
        'SURPRISED': 'SURPRESO',
        'CALM': 'CALMO',
        'FEAR': 'MEDO',
        # Adicione outras emoções conforme necessário
    }
    return mapa_emocoes.get(emocao_en, emocao_en) # Retorna original se não encontrar

def traduzir_genero(genero_en):
    mapa_genero = {
        'Male': 'Masculino',
        'Female': 'Feminino'
    }
    return mapa_genero.get(genero_en, genero_en)

def traduzir_booleano(valor_booleano):
    return 'Sim' if valor_booleano else 'Não'

# --- Rotas da API ---

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect(): # Renomeado de detect_old para detect
    data = request.json['image']
    # Remove o prefixo 'data:image/jpeg;base64,' ou similar
    try:
        header, encoded_data = data.split(',', 1)
        img_bytes = base64.b64decode(encoded_data)
    except (ValueError, TypeError, base64.binascii.Error) as e:
        print(f"Erro ao decodificar a imagem base64: {e}")
        return jsonify({'erro': 'Formato de imagem inválido ou erro na decodificação.'}), 400

    # Envia a imagem ao Rekognition
    try:
        response = client.detect_faces(
            Image={'Bytes': img_bytes},
            Attributes=['ALL']
        )
        faces = response.get('FaceDetails', []) # Usar .get para evitar KeyError
    except Exception as e:
        print(f"Erro ao chamar o Rekognition: {e}")
        # Considerar logar o erro completo para depuração interna
        return jsonify({'erro': 'Erro ao processar a imagem no serviço de reconhecimento.'}), 500

    resultados_pt = []
    for face in faces:
        # Traduzindo Emoções
        emocoes_pt = []
        for emocao in face.get('Emotions', []):
            emocoes_pt.append({
                'Tipo': traduzir_emocao(emocao.get('Type')),
                'Confianca': emocao.get('Confidence')
            })

        # Traduzindo Gênero
        genero_info = face.get('Gender', {})
        genero_pt = {
            'Valor': traduzir_genero(genero_info.get('Value')),
            'Confianca': genero_info.get('Confidence')
        }

        # Traduzindo atributos booleanos
        sorrindo_info = face.get('Smile', {})
        sorrindo_pt = {
            'Valor': traduzir_booleano(sorrindo_info.get('Value')),
            'Confianca': sorrindo_info.get('Confidence')
        }

        pelos_faciais_info = face.get('FacialHair', {})
        pelos_faciais_pt = {
            'Barba': traduzir_booleano(pelos_faciais_info.get('Beard', {}).get('Value')),
            'ConfiancaBarba': pelos_faciais_info.get('Beard', {}).get('Confidence'),
            'Bigode': traduzir_booleano(pelos_faciais_info.get('Mustache', {}).get('Value')),
            'ConfiancaBigode': pelos_faciais_info.get('Mustache', {}).get('Confidence')
        }

        olhos_abertos_info = face.get('EyesOpen', {})
        olhos_abertos_pt = {
            'Valor': traduzir_booleano(olhos_abertos_info.get('Value')),
            'Confianca': olhos_abertos_info.get('Confidence')
        }

        boca_aberta_info = face.get('MouthOpen', {})
        boca_aberta_pt = {
            'Valor': traduzir_booleano(boca_aberta_info.get('Value')),
            'Confianca': boca_aberta_info.get('Confidence')
        }

        # Montando o dicionário de informações da face em português
        face_info_pt = {
            'CaixaDelimitadora': face.get('BoundingBox'),
            'Confianca': face.get('Confidence'),
            'FaixaEtaria': face.get('AgeRange'),
            'Emocoes': emocoes_pt,
            'Genero': genero_pt,
            'Sorrindo': sorrindo_pt,
            'PelosFaciais': pelos_faciais_pt,
            'OlhosAbertos': olhos_abertos_pt,
            'BocaAberta': boca_aberta_pt,
            # Adicionar outros atributos conforme necessário, traduzindo chaves e valores
            # Ex: 'QualidadeImagem': face.get('Quality'), 'Pose': face.get('Pose')
        }
        resultados_pt.append(face_info_pt)

    return jsonify({'faces': resultados_pt})


if __name__ == '__main__':
    # Obtém a porta da variável de ambiente ou usa 8080 como padrão
    # É comum usar 8080 ou 5000 para desenvolvimento local
    port = int(os.environ.get('PORT', 80))
    # debug=True não é recomendado em produção
    app.run(host='0.0.0.0', port=port, debug=False) # Alterado debug para False e porta padrão para 8080

