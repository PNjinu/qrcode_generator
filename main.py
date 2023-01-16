import qrcode, qrcodegen, base64
from flask import Flask, render_template, request, send_file, session, make_response
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'Your secret key'

# Create QR code object
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr2 = ""
#data = ""


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form['data']
    session['data'] = data
    qr2 = qrcodegen.QrCode.encode_text(data, qrcodegen.QrCode.Ecc.HIGH)
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code object
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image in memory
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    session['img_io'] = img_io.read()
    img_io.seek(0)

    # This version can be displayed on browser
    img_base64 = base64.b64encode(img_io.getvalue()).decode()

    return render_template("generate.html", data=data, img_io=img_io, img_base64=img_base64, img=img)

@app.route('/download/<string:file_type>')
def download(file_type):
    data = session['data']
    if file_type == 'png':
        img_io = BytesIO(session.get('img_io'))
        img_io.seek(0)

        response = make_response(img_io.getvalue())
        response.headers["Content-Disposition"] = f"attachment; filename={data}.png"
        response.mimetype = 'image/png'
        return response

    elif file_type == 'svg':
        img_io = BytesIO(session.get('img_io'))
        img_io.seek(0)

        response = make_response(img_io.getvalue())
        response.headers["Content-Disposition"] = f"attachment; filename={data}.svg"
        response.mimetype = 'image/svg+xml'
        return response

if __name__ == '__main__':
    app.run(debug=True)
