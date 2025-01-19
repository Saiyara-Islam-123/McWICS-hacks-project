import pandas as pd
import naive_bayes

import numpy as np
import encode

df = pd.read_csv("fake_dataset.csv")

df = df.drop(columns=['store'])

def format(datestring):
    return datestring[:-5]

def encode_date(datestring):
    encoder = encode.Encoder()
    code = encoder.date_to_code[datestring]

    return code

def decode_date(c):
    encoder = encode.Encoder()
    date = encoder.code_to_date[c]
    return date

X_train = df["store id"].to_numpy().reshape(34, 1)
y_train = df["sale_date"].apply(format).apply(encode_date).to_numpy().reshape(34, 1)

model = naive_bayes.NaiveBayes(X_train, y_train)

def get_pred_and_prob(store, today_date):
    today = np.array([[encode_date(today_date)]])

    date, prob =  model.find_nearest_pred_sale_date_and_prob(np.array([[encode.encode_store(store)]]), today)
    return decode_date(date), prob

print(get_pred_and_prob("Zara", "7/9"))
