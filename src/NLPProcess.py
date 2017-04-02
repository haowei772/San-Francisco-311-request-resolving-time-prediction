import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

from nltk import pos_tag
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from PremodelingProcess import train_vali_split, get_df_for_modeling, dump_object_to_pickle, get_df_for_engineer, process_data_for_survival_model
from sklearn.cluster import KMeans


class NLPProcessor(object):

    def __init__(self, cluster_size):
        self.cluster_size = cluster_size
        self.tfidf = None
        self.tfidfed_train = None
        self.fit_transformed = False

    def process_docs(self, df, target_col):
        series_train = df[target_col].apply(lambda x: str(x).lower())
        content = list(series_train)

        # Create a set of tokenized documents.
        docs = [word_tokenize(content) for content in content]

        #Stemming / Lemmatization
        porter = PorterStemmer()
        docs_porter = [[porter.stem(word) for word in words] for words in docs]
        new_docs = [' '.join(doc) for doc in docs_porter]
        return new_docs

    def fit_transform(self, df, target_col):
        docs = self.process_docs(df, target_col)
        '''Make tfidf model and tfidfed matrix'''
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidfed_train = self.tfidf.fit_transform(docs)
        self.fit_transformed = True
        # '''save ftidf model to pickle file, will be used to transform the text in test file'''
        # filename_tfidf_pickle = '../data/SF311_tfidf.pickle'
        # filename_tfidfed_pickle = '../data/SF311_tfidfed.pickle'
        # dump_object_to_pickle(self.tfidf,filename_tfidf_pickle)
        # dump_object_to_pickle(self.tfidfed_train,filename_tfidfed_pickle)
        return self.tfidf

    def get_kmeans_train_labels(self):
        print 'Perform kmeans...'
        self.k_means = KMeans(n_clusters=self.cluster_size, n_jobs=-2)

        if self.fit_transformed:
            self.k_means.fit(self.tfidfed_train)
        else:
            print 'No valid tf-idf, need to fit_transform the training data!'
            return
        print len(self.k_means.labels_)
        print 'kmeans centers: ', self.k_means.cluster_centers_[:5]
        self.cluster_centers_ = self.k_means.cluster_centers_
        self.train_labels_ =  self.k_means.labels_
        return self.train_labels_

    def transform(self, df, target_col):
        docs = self.process_docs(df, target_col)
        self.tfidfed_test = self.tfidf.transform(docs)
        self.tfidfed_test_dense = self.tfidfed_test.todense()
        self.cosine_similarities = linear_kernel(self.tfidfed_test_dense, self.cluster_centers_)

        self.test_labels_ = np.argmax(self.cosine_similarities, axis =1)
        return self.test_labels_
