#https://www.kaggle.com/balatmak/text-preprocessing-steps-and-universal-pipeline
import string
import spacy 
import en_core_web_sm
import re
import numpy as np
import pandas as pd
import multiprocessing as mp
from nltk.tokenize import word_tokenize
from sklearn.base import TransformerMixin, BaseEstimator
from normalise import normalise
from nltk.corpus import stopwords

nlp = en_core_web_sm.load()


class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self,
                 variety="BrE",
                 user_abbrevs={},
                 n_jobs=1):
        self.variety = variety
        self.user_abbrevs = user_abbrevs
        self.n_jobs = n_jobs

    def fit(self, X, y=None):
        return self

    def transform(self, X, column,*_):
        """
        this method will be used in pre-processing which handle multi-processing
        """
        X_copy = X
        self.column = column

        partitions = 1
        cores = mp.cpu_count()
        if self.n_jobs <= -1:
            partitions = cores * 2
        elif self.n_jobs <= 0:
            return X_copy[column].apply(self._preprocess_text)
        else:
            partitions = min(self.n_jobs, cores)

        data_split = np.array_split(X_copy[column], partitions)
        pool = mp.Pool(cores)
        data = pd.concat(pool.map(self._preprocess_part, data_split))
        pool.close()
        pool.join()

        X_copy["processed_"+column] =  data

        return X_copy

    def _preprocess_part(self, part):
        return part.apply(self._preprocess_text)

    def _preprocess_text(self, text):
        """
        this method performs below tasks
        1. Html tags removal
        2. Url's removal
        3. Decontraction of the text
        4. Text normalization
        5. Punctuation removal
        6. Stop words removal
        """
        #converting text to lower case
        lower_text = self._lower_case(text)
        
        #removing html tags(and i'm not removing tags in title because we don't have any tags in the title)
        if self.column == 'title':
            html_remove_text = lower_text
        else:
            html_remove_text = self._html_tags_removal(lower_text)

        #Url's removal
        url_remove_text = self._remove_url(html_remove_text) 

        #Decontraction of the text
        decontracted_text = self._decontracted(url_remove_text)

        #Normalizing the text
        normalized_text = self._normalize(decontracted_text)

        #removing Punctuations
        doc = self._tokenize_text(normalized_text)
        removed_punct = self._remove_punct(doc)

        #removing Stop words
        removed_stop_words = self._remove_stop_words(removed_punct)
        return  re.sub(' +', ' ',' '.join(removed_stop_words))

    def _lower_case(self,text):
        return text.lower()
    
    def _html_tags_removal(self,text): #function to clean the word of any html-tags and make it lower Cases
        #removing code part from the text
        compiler = re.compile('<code>.*?</code>')
        text = re.sub(compiler, '', text)

        #removing content between 'a' tags 
        compiler = re.compile('<a.*?>.*?</a>')
        text = re.sub(compiler, '', text)

        #removing content between 'img' tags
        compiler = re.compile('<img.*?>.*?</img>')
        text = re.sub(compiler, '', text)

        #removing all tags
        compiler = re.compile('<.*?>')
        text = re.sub(compiler, ' ', text)

        #removing html special symbols
        compiler = re.compile('&.*;')
        text = re.sub(compiler, ' ', text)

        return text

    def _remove_url(self,text):
        #https://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python
        compiler = re.compile("^https?:\/\/.*[\r\n]*")
        text = re.sub(compiler, '', text)
        return text

    def _decontracted(self,text):
        # specific
        text = re.sub(r"won't", "will not", text)
        text = re.sub(r"can\'t", "can not", text)

        # general
        text = re.sub(r"n\'t", " not", text)
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"\'s", " is", text)
        text = re.sub(r"\'d", " would", text)
        text = re.sub(r"\'ll", " will", text)
        text = re.sub(r"\'t", " not", text)
        text = re.sub(r"\'ve", " have", text)
        text = re.sub(r"\'m", " am", text)
        text = re.sub(r"\n", "", text)
        return text

    def _tokenize_text(self,text):
        tokens = nlp.tokenizer(text)
        return [token.text.lower() for token in tokens if not token.is_space]

    def _normalize(self, text):
        # some issues in normalise package
        try:
            return ' '.join(normalise(text, variety=self.variety, user_abbrevs=self.user_abbrevs, verbose=False))
        except:
            return text

    def _remove_stop_words(self, doc):
        new_words = []
        for word in doc:
            if word not in stopwords.words('english'):
                new_words.append(word)
        return new_words

    def _remove_punct(self, doc):
        new_words = []
        for word in doc:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words
