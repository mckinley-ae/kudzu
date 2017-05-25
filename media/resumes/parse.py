import nltk, re, pprint, json 
import PyPDF2
import sys
from nltk.tokenize import *
from nltk.corpus import treebank
from bs4 import BeautifulSoup
from urllib import request

# information_extraction
# pdf_to_text
# html_to_text
# strip_text 
#
#
#


def information_extraction(text):
	sentences = nltk.sent_tokenize(text)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	grammar = "NP: {<DT>?<JJ>*<NN>}"
	cp = nltk.RegexpParser(grammar)
	result = cp.parse(sentence)
	print(result)



def pdf_to_text(path_to_file):
	pdfFileObj = open(path_to_file, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pdfReader.numPages
	pageObj = pdfReader.getPage(0)
	text = pageObj.extractText()
	return text
	

def html_to_text(url):
	url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
	html = request.urlopen(url).read().decode('utf8')
	text = BeautifulSoup(html, 'lxml').get_text()
	return text


def strip_text(text):
	tokens = word_tokenize(text)
	#strip emails
	email_regex = '[\w\.-]+@[\w\.-]+'
	email_match = []
	for email in re.findall(email_regex, text):
		email_match.append(email)
	#strip phone numbers
	phone_number_regex = '[0-9]{3}.{0,3}[0-9]{3}.[0-9]{4}'
	phone_number_match = []
	for number in re.findall(phone_number_regex, text):
		phone_number_match.append(''.join(filter(lambda x: x.isdigit(), number)))
	#split into sentences
	def parse_sentences(tokens):	
		sentences = []
		sentence = [] 
		for i in range(0, len(tokens)):
			if tokens[i] == '.':
				try:
					sentence.append(tokens[i])
					sentences.append(sentence)
					sentence = []
				except:
					return None
			else: 
				sentence.append(tokens[i])
		return sentences
	#TODO create new candidate object, need constructor
	#prepare candidate object
	candidate = {
		'first_name' : '',
		'last_name' : '',
		'url' : [],
		'email' : [],
		'phone' : [],
		'text' : []
		}
	#add parsed data to candidate object
	#email	
	for email in email_match:
		candidate['email'].append(email)
	#phone_number	
	for phone_number in phone_number_match:
		candidate['phone'].append(phone_number)
	#parse_sentences	
	for sentence in parse_sentences(tokens):
		trees = parser.nbest_parse(sentence)
		for tree in trees:
			print(tree)
		candidate['text'].append(sentence)
	#open and prepare text file
	name = 'sample_url'
	f = open(str(name + '.txt'), 'w')
	#write to file
	with f as outfile:
		json.dump(candidate, outfile, indent=2, sort_keys=True)
	f.close()



