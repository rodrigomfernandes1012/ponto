from flask import Flask, render_template, request
import socket
import os

app = Flask(__name__)

def imprimir_codigo_zpl(ip, porta, zpl_code):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, porta))
            s.sendall(zpl_code.encode())
            print("Código ZPL enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar o código ZPL: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/imprimir', methods=['POST'])
def imprimir():
    # Variável com o texto da empresa
    empresa_nome = "VDCLOG VITORIA DA CONQUISTA"

    # Código ZPL com a variável
    zpl_code = f"""
    ^XA
    ^CF0,30
    ^FO10,50^FD{empresa_nome}^FS
    ^FO0,135^GB680,1,3,B^FS ; LINHA
    ^FO610,0^GB240,120,140,B^FS ; CAIXA PRETA
    ^FO670,10^CF0,30^FR^FDMINUTA^FS 
    ^FO630,70^CF0,50^FR^FD1054809^FS 
    ^FO680,140^GB210,100,100,B^FS 
    ^FO710,170^CF0,50^FR^FD???^FS 
    ^FO10,170^CF0,30^FD??? - VDC LOG^FS
    ^FO0,240^GB880,1,3,B^FS ; LINHA
    ^FO10,220^CF0,20^FDDESTINO 19.852.860/0001-81^FS
    ^FO10,270^FDVDC LOG TRANSPORTE E LOGISTICA MULTIMODAL LTDA^FS
    ^FO10,320^FDAVENIDA RAFAEL SPINOLA, 100^FS
    ^FO10,370^FDZABELE^FS
    ^FO10,420^CF0,20^FCEP: 45078000TEL: (77) 3426-7150^FS
    ^FO10,470^FD??????? - ??^FS

    ^FO680,240^GB210,300,100,B^FS 
    ^FO700,280^CF0,100^FR^FWB^FD???^FS
    ^FWN 
    ^CF0,20
    ^FO0,500^GB880,1,3,B^FS ; LINHA
    ^FO10,520^FDDOC^FS
    ^FO10,570^FD1^FS
    ^FO0,550^GB880,1,3,B^FS ; LINHA
    ^FO0,500^GB880,1,3,B^FS ; LINHA
    ^FO610,500^GB240,120,140,B^FS ; CAIXA PRETA
    ^FO0,640^GB980,1,3,B^FS ; LINHA
    ^FO630,520^CF0,50^FR^FD001/010^FS 
    ^BY3,2,100
    ^FO0,650^BC^FD43030229864308742^FS
    ^FO10,790^CF0,20^FDCreado: 28/01/2025 às 15:20:10^FS
    ^XZ
    """

    # Substitua pelo IP e porta da sua impressora
    imprimir_codigo_zpl('192.168.0.200', 9100, zpl_code)
    return "Impressão enviada!"

#if __name__ == '__main__':
#    app.run(debug=True)


def main():
    port = int(os.environ.get("PORT", 80))
    # Escuta em todos os endereços IP disponíveis
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()