import requests
from parsel import Selector
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from heapq import nlargest
from collections import defaultdict
from nltk.probability import FreqDist

url = 'http://www.saopaulo.sp.gov.br/spnoticias/ultimas-noticias/centro-paula-souza-e-ibm-apresentam-modelo-educacional-p-tech/'
text = requests.get(url).text
selector = Selector(text=text)

title = selector.xpath('//header[contains(@class, "article-header")]//h1/text()').get()
legend = selector.xpath('//header[contains(@class, "article-header")]//p/text()').get()
paragraphs = selector.xpath('//article[contains(@class, "article-main")]//p/text()').getall()

text_to_analyse = ''

for paragraph in paragraphs:
    text_to_analyse += paragraph

sentences = sent_tokenize(text_to_analyse)
words = word_tokenize(text_to_analyse.lower())
stopwords = set(stopwords.words('portuguese') + list(punctuation))

words_without_stopwords = [word for word in words if word not in stopwords]

frequence = FreqDist(words_without_stopwords)

important_sentences = defaultdict(int)

for i, sentence in enumerate(sentences):
    for word in word_tokenize(sentence.lower()):
        if word in frequence:
            important_sentences[i] += frequence[word]
            

idx_important_sentences = nlargest(3, important_sentences, important_sentences.get)

print(title)
print(legend)
for i in sorted(idx_important_sentences):
    print(sentences[i])
