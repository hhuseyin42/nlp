import pandas as pd
import re
import snowballstemmer

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