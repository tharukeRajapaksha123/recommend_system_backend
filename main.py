import numpy as np
import pandas as pd
import re
import spacy
from keras import Sequential
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Dense, Dropout, Flatten, Bidirectional, Embedding, LSTM
from keras.utils import to_categorical, pad_sequences
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer


import string

apposV2 = {
    "are not": "are not",
    "ca": "can",
    "could n't": "could not",
    "did n't": "did not",
    "does n't": "does not",
    "do n't": "do not",
    "had n't": "had not",
    "has n't": "has not",
    "have n't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "i'd": "I would",
    "i'd": "I had",
    "i'll": "I will",
    "i'm": "I am",
    "is n't": "is not",
    "it's": "it is",
    "it'll": "it will",
    "i've": "I have",
    "let's": "let us",
    "might n't": "might not",
    "must n't": "must not",
    "sha": "shall",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "should n't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "we'd": "we would",
    "we're": "we are",
    "were n't": "were not",
    "we've": "we have",
    "what'll": "what will",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "where's": "where is",
    "who'd": "who would",
    "who'll": "who will",
    "who're": "who are",
    "who's": "who is",
    "who've": "who have",
    "wo": "will",
    "would n't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have",
    "'re": " are",
    "was n't": "was not",
    "we'll": "we will",
    "did n't": "did not"
}
appos = {
    "aren't": "are not",
    "can't": "cannot",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "i'd": "I would",
    "i'd": "I had",
    "i'll": "I will",
    "i'm": "I am",
    "isn't": "is not",
    "it's": "it is",
    "it'll": "it will",
    "i've": "I have",
    "let's": "let us",
    "mightn't": "might not",
    "mustn't": "must not",
    "shan't": "shall not",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "we'd": "we would",
    "we're": "we are",
    "weren't": "were not",
    "we've": "we have",
    "what'll": "what will",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "where's": "where is",
    "who'd": "who would",
    "who'll": "who will",
    "who're": "who are",
    "who's": "who is",
    "who've": "who have",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have",
    "'re": " are",
    "wasn't": "was not",
    "we'll": " will",
    "didn't": "did not"
}


def cleanData(reviews):
    all_ = []
    for review in reviews:
        lower_case = review.lower()  # lower case the text
        lower_case = lower_case.replace(" n't", " not")
        lower_case = lower_case.replace(".", " . ")
        lower_case = ' '.join(word.strip(string.punctuation) for word in lower_case.split())  # remove punctuation
        words = lower_case.split()  # split into words
        words = [word for word in words if word.isalpha()]  # remove numbers
        split = [apposV2[word] if word in apposV2 else word for word in
                 words]  # correct using apposV2 as mentioned above
        split = [appos[word] if word in appos else word for word in split]  # correct using appos as mentioned above
        split = [word for word in split if word not in stop]  # remove stop words
        reformed = " ".join(split)  # join words back to the text
        doc = nlp(reformed)
        reformed = " ".join([token.lemma_ for token in doc])  # lemmatiztion
        all_.append(reformed)
    df_cleaned = pd.DataFrame()
    df_cleaned['clean_reviews'] = all_
    return df_cleaned["clean_reviews"]


try:
    data = pd.read_csv('./tripadvisor_hotel_reviews.csv')
    X = data['Review'].copy()
    y = data['Rating'].copy()
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    stop = stopwords.words('english')
    X_cleaned = cleanData(X)

    encoding = {1: 0,
                2: 1,
                3: 2,
                4: 3,
                5: 4
                }
    labels = ['1', '2', '3', '4', '5']

    y = data['Rating'].copy()
    y.replace(encoding, inplace=True)
    y = to_categorical(y, 5)
    X_train, X_test, y_train, y_test = train_test_split(X_cleaned, y, test_size=0.4, random_state=1)
    # printing the shapes of the new X objects
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)
    X_train = tokenizer.texts_to_sequences(X_train)
    max_length = max([len(x) for x in X_train])
    vocab_size = len(tokenizer.word_index) + 1
    print("Vocabulary size: {}".format(vocab_size))
    print("Max length of sentence: {}".format(max_length))
    X_train = pad_sequences(X_train, max_length, padding='post')

    embedding_vector_length = 32
    num_classes = 5
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_vector_length, input_length=X_train.shape[1]))
    model.add(Bidirectional(LSTM(250, return_sequences=True)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    callbacks = [EarlyStopping(monitor='val_loss', patience=5),
                 ModelCheckpoint('../model/model.h5', save_best_only=True,
                                 save_weights_only=False)]
    history = model.fit(X_train, y_train, validation_split=0.11,
                        epochs=15, batch_size=32, verbose=1,
                        callbacks=callbacks)
    X_test_token = tokenizer.texts_to_sequences(X_test)
    X_test_token = pad_sequences(X_test_token, max_length, padding='post')
    pred = model.predict(X_test_token)
    pred = to_categorical(pred, 5)
    from sklearn.metrics import classification_report, accuracy_score
    print('Test Accuracy: {}'.format(accuracy_score(pred, y_test)))
    print(classification_report(y_test, pred, target_names=labels))
except Exception as e:
    print(f'error {e}')
