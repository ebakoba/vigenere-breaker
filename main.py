
from vigenere_crypto import crackCipherText
import json
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
        if len(cipher_text) < 100:
          return json.dumps({ 'message': 'Too short cipher text' }), 500
        try:
          result = crackCipherText(str(cipher_text).upper())
          return jsonify(result)
        except:
          return json.dumps({ 'message': 'Something went wrong in the server' }), 500

    return app

if __name__ == '__main__':
  app = make_app()
  app.run(port=8080)
