import operator
import sys

#cria dicionario com alfabeto passado
def createDict(alphabet):
    alphabetDict = dict()
    for char in alphabet:
        alphabetDict[char] = 0
    return alphabetDict

#le o arquivo a ser decifrado
def readFile(arq):
    f = open(arq, 'r')
    str = ''
    for line in f:
        str += line.rstrip('\n')
    return str

#escreve no arquivo decipheredText.txt a key usada e o texto decifrado
def writeFile(key, text):
    textFile = open('./decipheredText.txt', 'w')
    n = textFile.write('usedKey: ' + key + '\ntext: ' +text)
    textFile.close()

#conta as letras por um dicionario com o alfabeto
def counter(string, dictionary):
    for key in dictionary.keys():
        dictionary[key] = string.count(key)
    return dictionary

#calculo indice coincidencia
def coincidenceIndex(frequencies, total):
    freqSum = 0.0
    for value in frequencies.values():
        freqSum += value * (value - 1)
    ci = freqSum / (total * (total - 1))
    return ci

#divide as strings com as informacoes a serem checadas
def getDividedStrings(myText, keyLimit, alphabet):
    dividedStrings = []
    auxArray = []
    alphabetCounter = createDict(alphabet)
    for i in range(1, keyLimit + 1):
        for j in range(i):
            text = myText[j::i]
            total = len(text)
            #print('Key length:', i, 'Coincidence index: ', end='')
            endCount = counter(text, alphabetCounter)            
            letterMaxFreq = max(endCount.items(), key=operator.itemgetter(1))[0]
            result = coincidenceIndex(endCount, total)
            #print(result)
            auxArray.append({'keyLen': i, 'text': text, 'textLen': total, 'letterFrequency': letterMaxFreq, 'indexCoincidence': result})
        dividedStrings.append(auxArray)
        auxArray = []
    return dividedStrings

#checa o indice de coincidencia para pegar keyLength mais provavel
def checkCoincidenceIndex(dividedStrings):
    probKeys = []
    soma = 0
    counter = 1
    mean = 0
    for array in dividedStrings:
        for item in array:
            soma += item['indexCoincidence']
        mean = soma/(len(array))
        soma = 0
        probKeys.append((counter, mean))
        print('Key Length:', counter, 'Coincidence Index Mean:', mean)
        counter += 1
    return max(probKeys, key=lambda mean: mean[1])

#calcula distancia das letras 1 e 2 de um alfabeto
def letterDistance(letter1, letter2, alphabet):  
    letterIndex1 = alphabet.index(letter1)
    letterIndex2 = alphabet.index(letter2)
    
    if letterIndex2 >= letterIndex1:
        distance = letterIndex2 - letterIndex1
    else:
        distance = (letterIndex1 + letterIndex2) % 26
    
    return distance

#realiza analise de frequencia utilizando o metodo qui quadrado
def freqAnalysis(sequence, alphabet, language):
    lengthAlphabet = len(alphabet)
    lengthSequence = len(sequence)

    chiSquare = [0] * lengthAlphabet

    for i in range(lengthAlphabet):
        sumSquare = 0.0
        offset = []
        possibleValues = [0] * lengthAlphabet
        
        for j in range(lengthSequence):
            offset.append(chr(((ord(sequence[j])-ord('a')-i) % lengthAlphabet)+ord('a')))  

        for j in offset:
            possibleValues[ord(j) - ord('a')] += 1
        
        for j in range(lengthAlphabet):
            possibleValues[j] = possibleValues[j] / float(lengthSequence)
        
        for j in range(lengthAlphabet):
            sumSquare += ((possibleValues[j] - float(language[j][1])) * (possibleValues[j] - float(language[j][1])) / float(language[j][1]))

        chiSquare[i] = sumSquare
    moved = chiSquare.index(min(chiSquare))
    return chr(moved + ord('a'))

#decifra o texto armazena em uma string
def decipher(text, key, alphabet):
    decipheredText = ''
    countKey = 0
    for letter in text:
        if countKey == len(key):
            countKey = 0
        letterIndex1 = alphabet.index(letter)
        letterIndex2 = alphabet.index(key[countKey])
        if letterIndex1 + letterIndex2 >= 0:
            decipheredText += alphabet[letterIndex1 - letterIndex2]
        else:
            decipheredText += alphabet[letterIndex1 - letterIndex2+26]
        countKey+=1
    return decipheredText


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
englishFrequency = [('a', 0.082), ('b', 0.015), ('c', 0.028), ('d', 0.043), ('e', 0.127), ('f', 0.022), ('g', 0.02), ('h', 0.061),
 ('i', 0.07), ('j', 0.002), ('k', 0.008), ('l', 0.04), ('m', 0.024), ('n', 0.067), ('o', 0.075), ('p', 0.019),
 ('q', 0.001), ('r', 0.06), ('s', 0.063), ('t', 0.091), ('u', 0.028), ('v', 0.01), ('w', 0.023), ('x', 0.001),
 ('y', 0.02), ('z', 0.001)]

portugueseFrequency = [('a', 0.146), ('b', 0.01), ('c', 0.039), ('d', 0.05), ('e', 0.125), ('f', 0.01), ('g', 0.013), ('h', 0.013),
 ('i', 0.062), ('j', 0.008), ('k', 0.001), ('l', 0.028), ('m', 0.047), ('n', 0.044), ('o', 0.097), ('p', 0.025),
 ('q', 0.012), ('r', 0.065), ('s', 0.068), ('t', 0.043), ('u', 0.036), ('v', 0.015), ('w', 0.001), ('x', 0.004),
 ('y', 0.001), ('z', 0.004)]

myText = readFile(sys.argv[1])
KEY_LIMIT = int(sys.argv[2])
try:
    LANGUAGE = sys.argv[3]
except IndexError:
    LANGUAGE = ''
languageFrequency = []
if LANGUAGE == 'english':
    languageFrequency = englishFrequency
else:
    languageFrequency = portugueseFrequency

dividedStrings = getDividedStrings(myText, KEY_LIMIT, ALPHABET)
resultCoincidenceIndex = checkCoincidenceIndex(dividedStrings)
keyLength = resultCoincidenceIndex[0]
coincidenceIndex = resultCoincidenceIndex[1]
print('Found a possible Key Length:', keyLength, 'with Coincidence Index:', coincidenceIndex)

textInfo = dividedStrings[keyLength-1]

for index, sequence in enumerate(textInfo):
    print('Sequence:', index+1, 'Most frequent letter:', sequence['letterFrequency'])

keys = []
key = ''
for i, tup in enumerate(languageFrequency):
    print(tup[0],'[', i+1,']:', end=' ')
    for sequence in textInfo:
        calculatedLetter = ALPHABET[letterDistance(tup[0], sequence['letterFrequency'], ALPHABET)]
        key += calculatedLetter
        print(calculatedLetter, end=' ')
    keys.append(key)
    key = ''
    print('')

languageFreqSorted = sorted(languageFrequency, key=lambda freq: freq[1], reverse=True)

print('Choose one of the generated keys above to decipher your text')
print('Most frequent letters in your language:')
for i in range(5):
    indexAlphabet = languageFrequency.index(languageFreqSorted[i])
    print(languageFreqSorted[i], '[',indexAlphabet+1, ']', keys[indexAlphabet])

print('Calculating key using chi square...')
key = ''
for sequence in textInfo:
    keyLetter = freqAnalysis(sequence['text'], ALPHABET, languageFrequency)
    key += keyLetter
keys.append(key)
print('Chi Square Key [', len(keys),']:', key)
selectedKey = int(input(''))
key = keys[selectedKey-1]
print('Deciphering your text using the key: ', keys[selectedKey-1])
writeFile(key, decipher(myText, key, ALPHABET))
