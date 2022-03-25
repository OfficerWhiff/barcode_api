import flask
from flask import render_template, url_for, send_file
import os
import qrcode
from barcode import Code39
from barcode.writer import ImageWriter

app = flask.Flask(__name__,)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/barcode/<code>', methods=['GET'])
def generate_barcode(code):
    if not os.path.exists(f'static/barcode/{code}.png'):
        my_code = Code39(code, writer=ImageWriter(), add_checksum=False)
        my_code.default_writer_options['write_text'] = False
        my_code.save(f'static/barcode/{code}')
    barcode_filename = os.path.join(f'barcode/{code}.png')
    return send_file(f'static/{barcode_filename}', attachment_filename = barcode_filename)

@app.route('/api/qrcode/<code>', methods=['GET'])
def generate_qrcode(code):
    if not os.path.exists(f'static/qrcode/{code}.png'):
        # Make QRCode
        img = qrcode.make(code)
        img.save(f"static/qrcode/{code}.png")
    qr_filename = os.path.join(f'qrcode/{code}.png')
    return send_file(f'static/{qr_filename}', attachment_filename = qr_filename)

app.run(host='0.0.0.0')