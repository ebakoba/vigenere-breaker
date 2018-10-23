
import string
import os
from itertools import product
import concurrent.futures
import signal, psutil
from flask import Flask, render_template, request, jsonify

def kill_child_processes(parent_pid, sig=signal.SIGTERM):
  try:
    parent = psutil.Process(parent_pid)
  except psutil.NoSuchProcess:
    return
  children = parent.children(recursive=True)
  for process in children:
    process.send_signal(sig)

def generateBruteforceKeys(length):
  return [''.join(test) for test in product(string.ascii_uppercase, repeat=length)]
  

def calculateIndexOfCoincidence(text):
  text_length = len(text)
  alphabet = string.ascii_uppercase
  frequency_sum = 0
  
  for character in alphabet:
    frequency = text.count(character)
    frequency_sum += frequency * ( frequency - 1)
  index_of_coincidence = (1/(text_length * (text_length - 1))) * frequency_sum
  return index_of_coincidence

def findCosets(text, lenght):
  co_sets = []
  for _ in range(0, lenght):
    co_sets.append([])
  
  for index, character in enumerate(text):
    co_set_index = index % lenght
    co_sets[co_set_index].append(character)
  return co_sets

def cosetsIndexOfCoincidence(co_sets):
  indexes = []
  for co_set in co_sets:
    indexes.append(calculateIndexOfCoincidence(''.join(co_set)))
  avarage_coincidence = sum(indexes) / float(len(indexes))
  return avarage_coincidence

def getCoincidencesForKeyLengths(text, key_length_range):
  coincidences = []
  for lenght in key_length_range:
    coincidence = cosetsIndexOfCoincidence(findCosets(text, lenght))
    coincidences.append({'coincidence': coincidence, 'length': lenght})
  
  
  coincidences = sorted(coincidences, key=lambda k: k['coincidence'], reverse=True)
  lengths = [length_coincidence_pair['length'] for length_coincidence_pair in coincidences]
  return lengths

def decryptVigenerCypher(key, cipher_text):
  key = key.upper()
  alphabet = string.ascii_uppercase

  key_index = 0
  translated = []
  for character in cipher_text:
    number = alphabet.find(character)
    if number != -1:
      number -= alphabet.find(key[key_index])
    else:
      raise ValueError('An unrecongizable character in the cipher text')
  
    number %= len(alphabet)
    translated.append(alphabet[number])
    key_index += 1
    key_index %= len(key)

  return ''.join(translated)

def load_words(file_path):
  with open(file_path) as word_file:
      valid_words = set(word_file.read().split())
  return valid_words

def ensureCartesianProductFile(file_path):
  if not os.path.isfile(file_path):
    test_file = open(file_path, 'w')
    for test_string in generateBruteforceKeys(4):
      test_file.write('{}\n'.format(test_string))
    test_file.close()

def tryKeysFromFile(file_path, cipher_text):
  for key in load_words(file_path):
    index_of_coincidence = calculateIndexOfCoincidence(decryptVigenerCypher(key, cipher_text))
    if index_of_coincidence > 0.064:
      plain_text = decryptVigenerCypher(key, cipher_text)
      if plain_text.count('THE') > 5:
        return {
          'key': key.upper(),
          'plainText': plain_text
        }

def pureBruteForce(cipher_text):
  sorted_lenghts = getCoincidencesForKeyLengths(cipher_text, range(1, 10))
  for lenght in sorted_lenghts:
    directory = '.tmp'
    if not os.path.exists(directory):
      os.makedirs(directory)
    file_path = os.path.join(directory, 'cartprod_{}.txt'.format(lenght))
    for test_key in tryKeysFromFile(file_path, cipher_text):
      index_of_coincidence = calculateIndexOfCoincidence(decryptVigenerCypher(test_key, cipher_text))
      if index_of_coincidence > 0.064:
        break

def crackCipherText(cipher_text):
  tasks = [[tryKeysFromFile, './words/all.txt', cipher_text], [tryKeysFromFile, './words/10000-popular.txt', cipher_text], [pureBruteForce, cipher_text]]
  with concurrent.futures.ProcessPoolExecutor(max_workers=5) as worker_pool:
    result = {'key': 'could not decrypt', 'plainText': 'could not decrypt'}
    futures = [worker_pool.submit(*task) for task in tasks]
    for future in concurrent.futures.as_completed(futures):
      result = future.result()
      break
    kill_child_processes(os.getpid())
    return result

app = Flask(__name__)

def make_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('./index.html')

    @app.route('api/crack', methods = ['POST'])
    def decrypter():
        request.accept_mimetypes['application/json']
        cipher_text = request.get_json()['cipher_text']
        result = crackCipherText(cipher_text)
        return jsonify(result)

    return app

if __name__ == '__main__':
  app = make_app()
  app.run(port=8080)
