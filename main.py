
from vigenere_crypto import bruteforceCrack, frequencyCrack
import json
from flask import Flask, render_template, request, jsonify, render_template_string


app = Flask(__name__)

def make_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
      print(render_template_string('./card.html'))
      return render_template('./index.html')

    @app.route('/api/crack/frequency', methods = ['POST'])
    def frequencyCracker():
      request.accept_mimetypes['application/json']
      cipher_text = request.get_json()['cipher_text']
      if len(cipher_text) < 100:
        return json.dumps({ 'message': 'Too short cipher text' }), 500
      try:
        result = frequencyCrack(str(cipher_text).upper())
        return jsonify(result)
      except:
        return json.dumps({ 'message': 'Something went wrong in the server' }), 500
    
    @app.route('/api/crack/bruteforce', methods = ['POST'])
    def bruteforceCracker():
      request.accept_mimetypes['application/json']
      cipher_text = request.get_json()['cipher_text']
      if len(cipher_text) < 100:
        return json.dumps({ 'message': 'Too short cipher text' }), 500
      try:
        result = bruteforceCrack(str(cipher_text).upper())
        return jsonify([result])
      except:
        return json.dumps({ 'message': 'Something went wrong in the server' }), 500

    return app

if __name__ == '__main__':
  app = make_app()
  app.run(port=8080)
