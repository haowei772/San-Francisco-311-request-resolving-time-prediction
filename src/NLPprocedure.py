'''Deal with request type using tf-idf then clustering'''
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from PremodelingProcess import train_vali_split, get_df_for_modeling, \
dump_object_to_pickle, get_df_for_engineer, process_data_for_survival_model, train_test_df_split
import numpy as np
import pandas as pd

'''Check if there is pickle files of dataframe ready for load'''
filename_train_pickle = '../data/SF311_train.pickle'
filename_train = '../data/SF311_train.csv'
df = get_df_for_engineer(filename_train_pickle, filename_train)
print 'dataframe shape: ', df.shape
# print df.head()

#df['Request Type'] = df['Request Type'].apply(lambda x: str(x).lower())
#df1 = df[:1000]#run a pilot
df1 = df.copy()
df_tra, df_val = train_test_df_split(df1, test_size = 0.2, random_seed = 222)
series_tra = df_tra['Request Topic'].apply(lambda x: str(x).lower())
series_val = df_val['Request Topic'].apply(lambda x: str(x).lower())
documents_train = list(series_tra)
documents_validation = list(series_val)
print documents_train[:5]


# Tokenize and remove stop words

# 1. Create a set of documents.
#documents = [' '.join(article['content']).lower() for article in coll.find()]

# 2. Create a set of tokenized documents. No need to tokenize because there is no punctuation in the phrase
docs = [word_tokenize(content) for content in documents_train]
print docs[:15]

# # 3. Strip out stop words from each tokenized document.
# stop = set(stopwords.words('english'))
# docs = [[word for word in words if word not in stop] for words in docs]

# Stemming / Lemmatization

# 1. Stem using both stemmers and the lemmatizer
porter = PorterStemmer()

# snowball = SnowballStemmer('english')
# wordnet = WordNetLemmatizer()
docs_porter = [[porter.stem(word) for word in words] for words in docs]

# docs_snowball = [[snowball.stem(word) for word in words] for words in docs]
# docs_wordnet = [[wordnet.lemmatize(word) for word in words] for words in docs]

# print docs_porter[:30]
# print '*************'
new_docs = [' '.join(doc) for doc in docs_porter]
# print new_docs[:30]
#3. Create word count vector over the whole corpus.
cv = CountVectorizer(stop_words='english')
vectorized = cv.fit_transform(new_docs)

'''Make tfidf model and tfidfed matrix'''
tfidf = TfidfVectorizer(stop_words='english')
tfidfed = tfidf.fit_transform(documents_train)

#print tfidfed
'''save ftidf model to pickle file, will be used to transform the text in test file'''
filename_tfidf_pickle = '../data/SF311_tfidf.pickle'
filename_tfidfed_pickle = '../data/SF311_tfidfed.pickle'
dump_object_to_pickle(tfidf,filename_tfidf_pickle)
dump_object_to_pickle(tfidfed,filename_tfidfed_pickle)
print 'done tfidf'

dense = tfidfed.todense()
dense.shape

from sklearn.cluster import KMeans
k_means = KMeans(n_clusters=100, n_jobs=-2)
k_means.fit(tfidfed)
print len(k_means.labels_)
#print k_means.cluster_centers_[:5]
print type(k_means.cluster_centers_)
centers = k_means.cluster_centers_

df_tra['kmeans'] = k_means.labels_
df_tra.to_csv('../data/SF311_df_train_kmeans.csv')
#df_tra.head(30)

print documents_validation[:5]
valid_tfidfed = tfidf.transform(documents_validation)
valid_dense = valid_tfidfed.todense()

from sklearn.metrics.pairwise import linear_kernel
cosine_similarities = linear_kernel(valid_dense, centers)
cosine_similarities.shape
type(cosine_similarities)
validation_labels = np.argmax(cosine_similarities, axis =1)
print validation_labels.shape
print validation_labels[:10]
cosine_similarities[:10]
df_val['kmeans'] = validation_labels
print df_val.head(1)
df_val.to_csv('../data/SF311_df_test_kmeans.csv')

df_train_kmeans = pd.read_csv('../data/SF311_df_train_kmeans.csv')
df_test_kmeans = pd.read_csv('../data/SF311_df_test_kmeans.csv')
print df_train_kmeans.shape
print df_train_kmeans.info()
