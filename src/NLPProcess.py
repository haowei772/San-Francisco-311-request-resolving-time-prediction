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
dump_object_to_pickle, get_df_for_engineer, \
train_test_df_split, process_data_for_survival_model


'''Check if there is pickle files of dataframe ready for load'''
filename_train_pickle = '../data/SF311_train.pickle'
filename_train = '../data/SF311_train.csv'
df = get_df_for_engineer(filename_train_pickle, filename_train)
print 'dataframe shape: ', df.shape
#print df.head()

rt = df['Request Type'].apply(lambda x: str(x).lower())
documents = list(rt)[:1000]
print documents[:10]
'''$$$$$$$$$$'''

df = df[:1000]#run a pilot
df_train, df_test = train_test_df_split(df, test_size = 0.2, random_seed = 111)
rt = df_train['Request Type'].apply(lambda x: str(x).lower())
documents = list(rt)
print documents[:10]
# Tokenize and remove stop words

# 1. Create a set of documents.
#documents = [' '.join(article['content']).lower() for article in coll.find()]

# 2. Create a set of tokenized documents. No need to tokenize because there is no punctuation in the phrase
# docs = [word_tokenize(content) for content in documents]
# print docs[:15]

# # 3. Strip out stop words from each tokenized document.
# stop = set(stopwords.words('english'))
# docs = [[word for word in words if word not in stop] for words in docs]

# Stemming / Lemmatization

# 1. Stem using both stemmers and the lemmatizer
# porter = PorterStemmer()

# snowball = SnowballStemmer('english')
# wordnet = WordNetLemmatizer()
# docs_porter = [[porter.stem(word) for word in words] for words in documents]

# docs_snowball = [[snowball.stem(word) for word in words] for words in docs]
# docs_wordnet = [[wordnet.lemmatize(word) for word in words] for words in docs]

#print docs_porter[:30]

# 3. Create word count vector over the whole corpus.
# cv = CountVectorizer(stop_words='english')
# vectorized = cv.fit_transform(documents)

tfidf = TfidfVectorizer(stop_words='english')
tfidfed = tfidf.fit_transform(documents)

print tfidfed
'''save ftidf model to pickle file, will be used to transform the text in test file'''
filename_tfidf_pickle = '../data/SF311_tfidf.pickle'
filename_tfidfed_pickle = '../data/SF311_tfidfed.pickle'
dump_object_to_pickle(tfidf,filename_tfidf_pickle)
dump_object_to_pickle(tfidfed,filename_tfidfed_pickle)

# Cosine Similarity using TF-IDF
