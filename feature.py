from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import chi2
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np

df = pd.read_csv('csv/combined_csv.csv')
col = ['Id', 'Text', 'Topic' , 'processed_Text']
df = df[col]
df = df[pd.notnull(df['processed_Text'])]
category_id_df = df[['Topic', 'Id']].drop_duplicates().sort_values('Id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['Id', 'Topic']].values)

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(df.processed_Text.values.astype('U')) .toarray()
labels = df.Id

N = 2
for Topic, Id in sorted(category_to_id.items()):
  features_chi2 = chi2(features, labels == Id)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]

X_train, X_test, y_train, y_test = train_test_split(df['processed_Text'], df['Topic'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)

