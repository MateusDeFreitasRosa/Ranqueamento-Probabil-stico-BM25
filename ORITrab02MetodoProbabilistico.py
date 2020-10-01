import os
import math

#constantes:
k1 = 2
b = 0.75

dirDocs = "docs/" #Diretório dos documentos (Textos).
dirTerms = "terms/" #Diretório dos termos.
#Obs: **Não** é necessário ter a mesma quantidade de documentos(termos) e documentos(textos).

list_terms = []
LAVE = 0
N = 0

caracter_remove = ['.',',','?','!',';', ':', '(', ')'] #Limpeza de texto para a contagem de frequencia.

class Term:
    def __init__(self, word):
        self.word = word
        self.DF=0
        self.listOfDocuments = []
        self.timeApper = []

    def addNewDocument(self, doc): #Verifica se já existe o documento no objeto, se já existir apenas incrementa na frequencia do termo no determinado documento,
        #caso não exista, incrementa um novo documento e sua uma nova frequencia que irá relacionar com o o novo documento.
        local=-1
        for i in range(len(self.listOfDocuments)):
            if doc.name == self.listOfDocuments[i].name:
                local=i
                break

        if local == -1:
            self.listOfDocuments.append(doc)
            self.timeApper.append(1)
            self.DF += 1
        else:
            self.timeApper[i] += 1

    def getIDF(self, N): #Calcula o IDF do termo.
        if self.DF > 0:
            return math.log10((N / self.DF))
        return 0

    def freq_about_an_document(self, doc): #Pega a frequencia do termo em um documento.
        local = -1
        for i in range(len(self.listOfDocuments)):
            if doc.name == self.listOfDocuments[i].name:
                local = i
                break
        if local == -1:
            return 0
        return self.timeApper[local]


class Doc:
    def __init__(self, name, ):
        self.name = name
        self.LD = 0

    def plus_one(self):
        self.LD+=1


def addNewTerm(word): #Adiciona um novo termo na lista de objetos.
    exist = False
    for term in list_terms:
        if term.word == word:
            exist = True #ignore.
            break

    if not exist:
        new_term = Term(word)
        list_terms.append(new_term)


def getDocuments(dir): #Pega todos os documentos txt em um diretório definido no scopo.
    arquivos = []
    for filename in os.listdir(dir):
        if filename.endswith(".txt"):
            arquivos.append(filename)
            continue
        else:
            continue
    return arquivos


def updateTerm(word, doc):
    global LAVE, caracter_remove #define que essa função pode utilizar as variaveis globais.

    for remove in caracter_remove: #Remove pontuação, parentêses...
        while word.__contains__(remove):
            word = word.replace(remove, '')

    doc.plus_one() #incrementa o LD do documento.
    LAVE+=1
    for term in list_terms:
        if term.word == word:
            term.addNewDocument(doc)
            break

for documento in getDocuments(dirTerms): #Lendo termos e adicionando-os no objeto Terms
    arquivo = open(dirTerms+documento, 'r')
    for linha in arquivo:
        linha = linha[:-1] if linha[-1:] == '\n' else linha #Aqui removemos as possíveis quebras de linhas que possam vir do txt.
        for palavra in linha.lower().split(' '):
            addNewTerm(palavra) #Adicionando os termos no objeto.
    arquivo.close()

for documento in getDocuments(dirDocs): #Lendo os docs encontrando frequencia de termos, LD, DF, LAVE, N.
    arquivo = open(dirDocs+documento, 'r')
    doc = Doc(documento)
    N+=1
    for linha in arquivo:
        linha = linha[:-1] if linha[-1:] == '\n' else linha
        for palavra in linha.lower().split(' '):
            updateTerm(palavra, doc) #Atualiza o doc e adiciona no objeto termo.
            #É importante observar que dentro desse \for/ estamos modificando o objeto doc a toda iteração, incrementando seu LD.
            #Dessa forma todos os objetos que receberam esse objeto \doc/ terão o objeto doc atualizados, por questão de apontamento.
            #Isso nos permite uma grande facilidade no processamento dos dados, pois não temos que ficar atualizando os dados em varios locais.
    arquivo.close()

LAVE /=N
for term in list_terms:
    print('Term: {} DF: {} IDF: {} -> Documents: {}'.format(term.word,  term.DF, term.getIDF(N), ['(name: {} : ld: {} freq: {})'.format(docum.name, docum.LD, freq) for (docum, freq) in zip(term.listOfDocuments, term.timeApper)]))
print('LAVE: {} N: {}'.format(LAVE, N))

query = ''

while query != 'sair':
    print('INFORME SUA CONSULTA: (Para sair digite sair).')
    query = input()

    terms_query = []
    documents_query = []

    if query != 'sair':
        #Aqui separamos os (termos x documentos) da consulta para a aplicação do modelo probabilístico.
        #Isso vai permitir uma boa estruturação e facilidade de entendimento do código quando formos aplicar o modelo probabilístico.
        for cons in query.lower().split():
            for term in list_terms:
                if term.DF > 0 and cons == term.word: #Caso o DF do termo seja 0 ignoramos, pois ele não aparece em nenhum documento de texto.
                    terms_query.append(term)
                    for doc in term.listOfDocuments:
                        exist = False
                        for doc_query in documents_query:
                            if doc_query.name == doc.name:
                                exist = True
                                break
                        if not exist:
                            documents_query.append(doc)

        print(['{}'.format(term.word) for term in terms_query])
        print(['{}'.format(documents.name) for documents in documents_query])

        #Calculando RVSd
        RVSd = []
        for docm_q in documents_query:
            probability = []
            for terms_q in terms_query:
                kx = (k1+1)* terms_q.freq_about_an_document(docm_q)
                ky = k1* ((1-b) +b * (docm_q.LD/LAVE)) + terms_q.freq_about_an_document(docm_q)
                probability.append(terms_q.getIDF(N) * (kx/ky))
            RVSd.append(sum(probability))

        rank = zip(documents_query, RVSd) #É mesclado documentos x RVSd para mostrar os dados ordenados.
        rank = sorted(rank, key=lambda x: x[1], reverse=True) #Ordenação em relação ao RVSd.

        print('****************Rankeamento***************')
        i=1
        for rankeamento in rank:
            print('{}º: Documento: {} -> RSVd: {}'.format(i,rankeamento[0].name, rankeamento[1]))
            i+=1

