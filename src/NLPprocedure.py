'''Deal with 'Request type' by convert the text script into tf-idf then do k-means clustering on the tf-idf to generate categories of requests'''
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from PremodelingProcess import train_vali_split, get_df_for_modeling, \
dump_object_to_pickle, get_df_for_engineer, train_test_df_split

from sklearn.metrics.pairwise import linear_kernel
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd


if __name__ == '__main__':
    '''Check if there is pickle files of dataframe ready for load'''
    filename_train_pickle = '../data/SF311_train.pickle'
    filename_train = '../data/SF311_train.csv'
    df = get_df_for_engineer(filename_train_pickle, filename_train)

    df1 = df.copy()
    df_tra, df_val = train_test_df_split(df1, test_size = 0.2, random_seed = 222)
    series_tra = df_tra['Request Topic'].apply(lambda x: str(x).lower())
    series_val = df_val['Request Topic'].apply(lambda x: str(x).lower())
    documents_train = list(series_tra)
    documents_validation = list(series_val)

    '''Tokenize and remove stop words'''

    '''Create a set of tokenized documents. No need to tokenize because there is no punctuation in the phrase'''
    documents = [word_tokenize(content) for content in documents_train]

    '''Strip out stop words from each tokenized document'''
    stop = set(stopwords.words('english'))
    docs = [[word for word in words if word not in stop] for words in documents]

    '''Stemming / Lemmatization'''
    porter = PorterStemmer()
    docs_porter = [[porter.stem(word) for word in words] for words in docs]
    new_docs = [' '.join(doc) for doc in docs_porter]

    '''Create word count vector over the whole corpus'''
    cv = CountVectorizer(stop_words='english')
    vectorized = cv.fit_transform(new_docs)

    '''Make tfidf model and tfidfed matrix'''
    tfidf = TfidfVectorizer(stop_words='english')
    tfidfed = tfidf.fit_transform(documents_train)

    '''save ftidf model to pickle file, will be used to transform the text in test file'''
    filename_tfidf_pickle = '../data/SF311_tfidf.pickle'
    filename_tfidfed_pickle = '../data/SF311_tfidfed.pickle'
    dump_object_to_pickle(tfidf,filename_tfidf_pickle)
    dump_object_to_pickle(tfidfed,filename_tfidfed_pickle)
    print 'Tf-idf generation finished'

    dense = tfidfed.todense()
    dense.shape

    ''' Do k-means clustering of the tf-idf'''
    k_means = KMeans(n_clusters=100, n_jobs=-2)
    k_means.fit(tfidfed)
    centers = k_means.cluster_centers_
    df_tra['kmeans'] = k_means.labels_
    df_tra.to_csv('../data/SF311_df_train_kmeans.csv')

    valid_tfidfed = tfidf.transform(documents_validation)
    valid_dense = valid_tfidfed.todense()

    cosine_similarities = linear_kernel(valid_dense, centers)
    validation_labels = np.argmax(cosine_similarities, axis =1)
    df_val['kmeans'] = validation_labels

    df_val.to_csv('../data/SF311_df_test_kmeans.csv')

    df_train_kmeans = pd.read_csv('../data/SF311_df_train_kmeans.csv')
    df_test_kmeans = pd.read_csv('../data/SF311_df_test_kmeans.csv')
