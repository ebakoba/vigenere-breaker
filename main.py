
import string


cipher_text = 'STOMZLATLPQBSUOUAVZHYPGMSURTHOMLAJWLLHFXKPHMAUUBFHGMJLSMKPRXUHTXOHHVZPBZHLCIDLUHAUUBFHBWUVABFNCNLVTTZVILWVBMZLCMZLFLAKSHXAVXKAFXWATBJZHMZLMLWLHPGWSHHSSZGPBZAUHHLOSAGBGXLPAXHHGLWZOYLLFTOOWEWAVXQUCMAJSMZYSXHLFLGUGVGTWGYVIMGMHAWOCNKLHAWWVRKPQBKAGTQZHAWPBBLPOEELOLMYSFWUHPSZBMSJQNJHHXLOSUAVZHYPGMKHMLLOSRZHJXJLDKGKIVWKHAWTOMZLATLPQBSUGTQZWYWEOVLSMHFLDXJZCGWUHXJZHAWOCNKLHAWUWMOPZETLSFHAMTYHWGOOSGZLBKQRWLKPBZWYZXXAVTJCOKVHBWOLBMLVKTKOWGYACGLVGXJCSBFAVXFPLHFHRFAUWLLYOMAVBAWDOLSZYXVIMHFLVBKUSPUVZEWHUNWZOUGBHMZLDHDAWVSSWGXPUALPBZAUOVSKSFAHWGOHGAAUUMGUKXJLTTEVILXVFIGSWMAJOEAUHKANIXAAGHMYXHTZCFWVBXSZYXVIIMOLFXHPYXJZQHEWOKWKHHLOSUSJYLLHPUAUUTFKRBJAMIGSWMAJGTLBBBNLFLAAWXKDVRVVMHMWSHHSSYANVMDPYXLOOMCPGLAUUXJPGLSPRMGOOOWYSLHVBWWKWGZPGEGDUKSCSEDFJHAJSBLZPXUHILWAVXKAODWZOKWZCEGD'

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

for lenght in range(1, 20):
  coincidence = cosetsIndexOfCoincidence(findCosets(cipher_text, lenght))
  print(lenght, '-', coincidence)


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

def load_words(filename):
    with open('./words/{}'.format(filename)) as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


'''
for key in load_words('10000-popular.txt'):
  index_of_coincidence = calculateIndexOfCoincidence(decryptVigenerCypher(key, cipher_text))
  if index_of_coincidence > 0.064:
    print(index_of_coincidence)
    print(decryptVigenerCypher(key, cipher_text))
    break

for key in load_words('all.txt'):
  index_of_coincidence = calculateIndexOfCoincidence(decryptVigenerCypher(key, cipher_text))
  if index_of_coincidence > 0.064:
    print(index_of_coincidence)
    print(decryptVigenerCypher(key, cipher_text))
    break

'''