import argparse
import configparser


parser = argparse.ArgumentParser()
cfgParser = configparser.ConfigParser()
parser.add_argument("--model")
parser.add_argument("--config")
parser.add_argument("--train", default=False, action='store_true')
args = parser.parse_args()

cfgParser.read(args.config)

import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import mail
import time
import os, sys
import json
from tensorflow import keras
from keras.models import load_model
from tensorflow.keras import layers



stemmer = LancasterStemmer()

with open(args.model) as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

labels = ["important", "not important"]

def convertbag(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for w in s_words:
        for i, word in enumerate(words):
            if w == word:
                bag[i] = 1
    return np.array(bag)

for i in data['important']:
    wrd = nltk.word_tokenize(i)
    docs_x.append(wrd)
    words.extend(wrd)
    docs_y.append('important')

for i in data["not important"]:
    wrd = nltk.word_tokenize(i)
    docs_x.append(wrd)
    words.extend(wrd)
    docs_y.append('not important')


words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))
labels = sorted(labels)


training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)


#print(words, docs_x, docs_y, labels)
print(len(training[0]), output[0])


if args.train:
    #### train model
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 30)
    net = tflearn.fully_connected(net, 30)
    net = tflearn.fully_connected(net, 30)
    net = tflearn.fully_connected(net, 30)
    net = tflearn.fully_connected(net, 30)
    net = tflearn.fully_connected(net, 30)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    model.fit(training, output, n_epoch=2000, batch_size=8, show_metric=False)
    model.save('mail.h5')

else:
    #### load model
    model = load_model('mail.h5')
    model.compile(optimizer="Adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()

def predict(s, model):

    bag = convertbag(s, words)
    results = model.predict(np.array([bag]))
    if results[0][0] > 0.8:
        return True
    elif results[0][1] > 0.8:
        return False
    else:
        return None
    return results

def notify(title, m):
    os.system(f'terminal-notifier -message "{m[1]}" -title "{title}" -subtitle "{m[0]}"')
    # os.system(f"terminal-notifier -message {m[1]}")


oldmails = []
banner = """

                        ███╗   ███╗ █████╗ ██╗██╗         ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗
                        ████╗ ████║██╔══██╗██║██║         ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
                        ██╔████╔██║███████║██║██║         ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
                        ██║╚██╔╝██║██╔══██║██║██║         ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
                        ██║ ╚═╝ ██║██║  ██║██║███████╗    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
                        ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                    -- Hello Daniel!
\n
"""


old = []
while True:
    mails = mail.read_email_from_gmail(cfgParser.get("config", "mail"), cfgParser.get("config", "password"), 'UnSeen')
    os.system("clear")
    print(banner)
    if len(old) == 0:
        old = mails
    for m in mails:
        content = predict(m[1], model)
        sender = predict(m[0], model)


        if (content or sender):
            if m not in old:
                notify("Important mail!", m)
            print(f"important mail from \t{m[0]}: \t{m[1]}\n")

    old = mails
    oldmails = mails
    for i in range(5):
        print('.', end = "")
        sys.stdout.flush()
        time.sleep(1)
    print('loading', end = "")
    sys.stdout.flush()

try:
    pass


except:
    print("\nReceived keyboard interrupt, existing...\n")
