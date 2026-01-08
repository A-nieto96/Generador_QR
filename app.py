from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_generador = False
    return render_template('index.html', qr_generated=qr_generador)

@app.route('/generate', methods=['POST'])
def generador_qr():
    data = request.form.get('data')

    if not data:
        return "No se recibió ningún texto o URL para generar el QR", 400

    # Crear el QR
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar la imagen en memoria (no en disco)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Devolver la imagen como archivo descargable
    return send_file(
        buffer,
        as_attachment=True,
        download_name="codigo_qr.png",
        mimetype="image/png"
    )

if __name__ == '__main__':
    app.run(debug=True)
