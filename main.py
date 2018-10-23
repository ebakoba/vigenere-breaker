
from vigenere_crypto import crackCipherText
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def make_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('./index.html')

    @app.route('/api/crack', methods = ['POST'])
    def decrypter():
        request.accept_mimetypes['application/json']
        cipher_text = request.get_json()['cipher_text']
        result = crackCipherText(cipher_text)
        return jsonify(result)

    return app

if __name__ == '__main__':
  app = make_app()
  app.run(port=8080)
