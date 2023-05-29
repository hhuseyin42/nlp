import pandas as pd
import re
import snowballstemmer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec

# sayısal değerlerin kaldırılması
def remove_numeric(value):
    bfr= [item for item in value if not item.isdigit()]
    bfr="".join(bfr)
    return bfr

text="Nida Cakmak 123"
remove_numeric(text)

#emojilerin kaldırılması
def remove_emoji(value):
    bfr=re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    bfr=bfr.sub(f'',value)
    return bfr

text="Nida Cakmak 🔎"
remove_emoji(text)

#tek karakterli ifadelerin kaldırılması
def remove_single_character(value):
    return re.sub(r'(?:^| )\w(?:$| )','',value)
text="Nida Cakmak h"
remove_single_character(text)

#noktalama işaretlerinin kaldırılması
def remove_noktalama(value):
    return re.sub(r'[^\w\s]','',value)

text= "Nida Cakmak ."
remove_noktalama(text)

#linklerin kaldırılması
def remove_link(value):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',value)

text= "Nida https://www.nedir.com/wikipedia"
remove_link(text)

#hashtaglerin kaldırılması
def remove_hashtag(value):
    return re.sub(r'#[^\s]+','',value)

text= "Nida #nlp"
remove_hashtag(text)

#kullanıcı adlarının kaldırılması
def remove_username(value):
    return re.sub('@[^\s]+','',value)

text="Nida @nidackmk"
remove_username(text)

#kök indirgeme ve stop words işlemi
def stem_word(value):
    stemmer=snowballstemmer.stemmer("turkish")
    value=value.lower()
    value=stemmer.stemWords(value.split())
    stop_words=['acaba','ama','aslında']
    value= [item for item in value if not item in stop_words]
    value=' '.join(value)
    return value

def pre_processing(value):
    return [remove_numeric(
        remove_emoji(
            remove_single_character(
                remove_noktalama(
                    remove_link(
                        remove_hashtag(
                            remove_username(
                                stem_word(word)))))))) for word in value.split()]
  
    
#boşlukların kaldırılması
def remove_space(value):
    return [item for item in value if item.strip()]


#bag of words model
def bag_of_words(value):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(value)
    return X.toarray().tolist()


#tf-ıdf model
def tfidt(value):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(value)
    return X.toarray().tolist()

#word2vec model
def word2vec(value):
    model = Word2Vec.load("../data/word2vec.model")
    bfr_list = []
    bfr_len = len(value)

    for k in value:
        bfr = model.wv.key_to_index[k]
        bfr = model.wv[bfr]
        bfr_list.append(bfr)

    bfr_list = sum(bfr_list)
    bfr_list = bfr_list / bfr_len
    return bfr_list.tolist()