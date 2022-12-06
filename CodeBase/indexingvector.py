
# import statements # 

from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pandas as pd
from nltk.corpus import stopwords
import json

# Method for vector space model
def vectorSpaceModel(query):

    f = open('corpusUnt.json')
    corpusJsonData = json.load(f)
    print(corpusJsonData)

    openCorpusInfo = open('corpusInfo.txt', 'r') #  corpusInfo.txt has all the valid URL and Content 
    corpusData = openCorpusInfo.readlines() # Reading corpus file
    stopWords = set(stopwords.words('english')) #Setting stopwords
    nltk.download('punkt')
    nltk.download('stopwords')
    def toGenerateTokens(LinkData):
    # generateTokens by reading LinkData using nltk
        tokenData = nltk.word_tokenize(LinkData)
        return tokenData

    def wordStemmer(tokenList):
    # wordStemmer using SnowballStemmer to remove inflexional ending
        stemmedWord = nltk.stem.SnowballStemmer("english")
        stemmed = []
        for words in tokenList:
            stemmed.append(stemmedWord.stem(words))
        return stemmed

    def toReadStopWords(LinkData):
    # toReadStopWords from LinkData
        CleanContent = []
        for token in LinkData:
            if token not in stopWords:
                CleanContent.append(token)
        return CleanContent

    tokenData = toGenerateTokens(corpusData[1])
    LinkData = toReadStopWords(tokenData)
    LinkData = wordStemmer(LinkData)
    document = ' '.join(LinkData)

    ModifiedCorpus = []
    for data in corpusData:
        tokenData = toGenerateTokens(data)
        LinkData = toReadStopWords(tokenData)
        LinkData = wordStemmer(LinkData)
        LinkData = ' '.join(LinkData)
        ModifiedCorpus.append(LinkData) # This contains data after preprocessing stage
        
    vectorizerX = TfidfVectorizer(stop_words='english')
    documentVector = vectorizerX.fit_transform(ModifiedCorpus)
    dataFrame = pd.DataFrame(documentVector.toarray(),
                       columns=vectorizerX.get_feature_names_out())

    query = toGenerateTokens(query)
    query = toReadStopWords(query)
    queryData = []
    for word in wordStemmer(query):
        queryData.append(word)
    queryData = ' '.join(queryData)
    queryVector = vectorizerX.transform([queryData])
    #Using cosineSimilarities to find similarity between query and existing link and content 
    cosineSimilarityValues = cosine_similarity(documentVector, queryVector).flatten()
    #Top 11 documents will be displayed on the top
    topScoredDocuments = cosineSimilarityValues.argsort()[:-12:-1]

    toBeDisplayedDocuments = []
    #This loop returns documents which will be displayed
    for index in topScoredDocuments:
        if 'link :' in ModifiedCorpus[index-1]:
            link = corpusData[index-1].replace("Link:", " ")
            linkData = corpusData[index].replace("Doc:", "")
            obj = {
                'link': link,
                'doc': linkData
            }
            toBeDisplayedDocuments.append(obj)

    return toBeDisplayedDocuments
