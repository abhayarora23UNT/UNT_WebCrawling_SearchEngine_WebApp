from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pandas as pd
from nltk.corpus import stopwords


def vectorModel(query):
    print("Query: " + query)
    open_file = open('corpus.txt', 'r')
    corpus = open_file.readlines()

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)

    vector = X
    df1 = pd.DataFrame(
        vector.toarray(), columns=vectorizer.get_feature_names_out())
    df1

    nltk.download('punkt')
    nltk.download('stopwords')

    stop_words = set(stopwords.words('english'))

    def get_tokenized_list(doc_text):
        tokens = nltk.word_tokenize(doc_text)
        return tokens

    def word_stemmer(token_list):
        ps = nltk.stem.SnowballStemmer("english")
        stemmed = []
        for words in token_list:
            stemmed.append(ps.stem(words))
        return stemmed

    def remove_stopwords(doc_text):
        cleaned_text = []
        for words in doc_text:
            if words not in stop_words:
                cleaned_text.append(words)
        return cleaned_text

    tokens = get_tokenized_list(corpus[1])

    doc_text = remove_stopwords(tokens)

    doc_text = word_stemmer(doc_text)
    doc_text

    doc_ = ' '.join(doc_text)
    print("Document in vsm", doc_)

    cleaned_corpus = []
    for doc in corpus:
        tokens = get_tokenized_list(doc)
        doc_text = remove_stopwords(tokens)
        doc_text = word_stemmer(doc_text)
        doc_text = ' '.join(doc_text)
        cleaned_corpus.append(doc_text)
    # cleaned_corpus
    print("cleaned_corpus", cleaned_corpus)

    vectorizerX = TfidfVectorizer(stop_words='english')
    vectorizerX.fit(cleaned_corpus)
    print("cleaned_corpus", cleaned_corpus)
    doc_vector = vectorizerX.transform(cleaned_corpus)
    print("Meghana123", doc_vector)
    doc_vector1 = vectorizerX.fit_transform(cleaned_corpus)
    print("doc_vector", doc_vector1)

    df1 = pd.DataFrame(doc_vector.toarray(),
                       columns=vectorizerX.get_feature_names_out())
    print("DataFrame", df1)

    df2 = pd.DataFrame(doc_vector1.toarray(),
                       columns=vectorizerX.get_feature_names_out())
    print("DataFrame1", df2)

    query = get_tokenized_list(query)
    print("AfterTokeniization", query)
    query = remove_stopwords(query)
    print("AfterStopWord", query)
    q = []
    for w in word_stemmer(query):
        q.append(w)
    q = ' '.join(q)
    print("q", q)
    query_vector = vectorizerX.transform([q])
    print("query_vector", query_vector)
    cosineSimilarities = cosine_similarity(doc_vector, query_vector).flatten()
    print("cosineSimilarities", cosineSimilarities)
    related_docs_indices = cosineSimilarities.argsort()[:-12:-1]
    print("related_docs_indices", related_docs_indices)
    print(related_docs_indices)

    results = []

    for i in related_docs_indices:
        if 'link :' in cleaned_corpus[i-1]:
            link = cleaned_corpus[i-1].replace("link : ", "")
            doc = corpus[i].replace("Doc:", "")

            obj = {
                'link': link,
                'doc': doc
            }
            results.append(obj)

    return results
