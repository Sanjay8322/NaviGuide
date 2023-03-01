import nltk
import numpy as np

# nltk.download('punkt')  #package for pre trained tokenizer 

from nltk.stem.porter import PorterStemmer  #used for stemming of words there also different stemmers available here we using porterStemmer
stemmer=PorterStemmer() 

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence,all_words):
    tokenized_sentence=[stem(w) for w in tokenized_sentence]
    bag=np.zeros(len(all_words),dtype=np.float32) #array of zeroes
    for idx,w in enumerate(all_words): #This will give index and words
        if w in tokenized_sentence:
            bag[idx]=1.0 
                            
    return bag
















# sentence=["hello","how","are","you"]
# words=["hi","hello","I","you","bye","thank","cool"]
# bog=bag_of_words(sentence,words)
# print(bog)

    
# a='haha hehe frrrrr'
# print(a)
# a=tokenize(a)
# print(a) 


# words=['Organize','organizes','organizing']
# stemmed_words=[stem(w) for w in words]
# print(stemmed_words)