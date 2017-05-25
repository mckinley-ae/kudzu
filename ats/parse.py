import nltk, re, pprint, json, PyPDF2
import sys
from nltk.tokenize import *
from nltk.corpus import treebank
from bs4 import BeautifulSoup
from urllib import request

## TODO
## implement validation for file types
## implement handling for each type of document uploaded
## parse variables out of documents
##



def pdf_to_text(pdf):
	pdfReader = PyPDF2.PdfFileReader(pdf)
	pdfReader.numPages
	pageObj = pdfReader.getPage(0)
	text = pageObj.extractText()
	return text

def information_extraction(text):
	sentences = nltk.sent_tokenize(text)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	grammar = "NP: {<DT>?<JJ>*<NN>}"
	cp = nltk.RegexpParser(grammar)
	result = cp.parse(sentence)
	print(result)


def html_to_text(url):
	url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
	html = request.urlopen(url).read().decode('utf8')
	text = BeautifulSoup(html, 'lxml').get_text()
	return text


def strip_text(text):
	tokens = word_tokenize(text)
	email_regex = '[\w\.-]+@[\w\.-]+'
	phone_number_regex = '[0-9]{3}.{0,3}[0-9]{3}.[0-9]{4}'
	date_regex = '\d{2,4}'
	name_regex = '([A-Z][A-Za-z]+)(\s+([A-Z][A-Za-z]+))'
	url_regex = '#((https?://|ftp://|www\.|[^\s:=]+@www\.).*?[a-z_\/0-9\-\#=&])(?=(\.|,|;|\?|\!)?("|«|»|\[|\s|\r|\n|$))'
	technology_regex = ''
	#https://mathiasbynens.be/demo/url-regex
	candidate = {
        'name' : '',
        'url' : [],
        'email' : [], ##  works
        'phone' : [], ## works
        'text' : []
    }
	#strip baseline text
	for block in re.split(r'\n{1,}', text):
		candidate['text'].append(block)
	#strip emails
	for email in re.findall(email_regex, text):
		candidate['email'].append(email)
	#strip phone numbers
	for number in re.findall(phone_number_regex, text):
		candidate['phone'].append(''.join(filter(lambda x: x.isdigit(), number)))
	#add first_name / last_name to candidate object
	candidate['name'] = re.split(name_regex, candidate['text'][0])
	#strip urls
	for url in re.findall(url_regex, text):
		candidate['url'].append(url)
	return candidate


	#parse_sentences
    #parser = nltk.ChartParser(grammar)
	#for sentence in parse_sentences(tokens):
	#	trees = parser.nbest_parse(sentence)
	#	for tree in trees:
	#		print(tree)
	#	candidate['text'].append(sentence)
	#open and prepare text file
	#name = 'sample_url'
	#f = open(str(name + '.txt'), 'w')
	#write to file
	#with f as outfile:
	#	json.dump(candidate, outfile, indent=2, sort_keys=True)
	#f.close()
    #split into sentences
    #def parse_sentences(tokens):
    	#sentences = []
    #		sentence = []
    #		for i in range(0, len(tokens)):
    #			if tokens[i] == '.':
    #				try:
    #					sentence.append(tokens[i])
    #					sentences.append(sentence)
    #					sentence = []
    #				except:
    #					return None
    #			else:
    #				sentence.append(tokens[i])
    #		return sentences
