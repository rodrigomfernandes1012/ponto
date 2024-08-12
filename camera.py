from flask import Flask, render_template, Response, request, flash, redirect
import cv2
from datetime import datetime

app = Flask(__name__)
video = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

@app.route('/')
def index():
    """Posicione o QR Code em frente a camera."""
    return render_template('index.html')

@app.route('/ponto')
def ponto():
    """Ponto Registrado!"""
    return render_template('ponto.html')

@app.route('/takeimage', methods = ['POST'])
def takeimage():
    name = request.form['name']
    print(name)
    _, frame = video.read()
    cv2.imwrite(f'{name}.jpg', frame)

    return Response(status = 200)



def gen():
    """Posicione o QR Code em frente a camera."""
    while True:
        variavel, frame = video.read()
        cv2.imwrite('t.jpg', frame)
        _, img = video.read()
        data, bbox, _ = detector.detectAndDecode(img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n')  + open('t.jpg', 'rb').read() + b'\r\n'
        if data:
            IDFunc = data
            print(str(datetime.now()) + " - SUCESSO! - Leitura de QR com sucesso. ID identificado: " + IDFunc)
            exit()




     #   cv2.imshow("QRCODEscanner", img) abre segunda tela

        # Linha para parar leitura com uma tecla. Não necessária
        if cv2.waitKey(1) == ord("q"):
            #print( str(datetime.now()) + " - AVISO! - Leitura de QR cancelada.")
            # os.system("start cmd /c python LerEscrever.py")
            # exit()
            break
    video.release()
    cv2.destroyAllWindows()


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
    app.debug = True