from sklearn.naive_bayes import MultinomialNB
import numpy as np

class NaiveBayes:
    def __init__(self, X_train, y_train): #X_train: store, y_train: date
        self.X_train = X_train
        self.y_train = y_train
        self.model = MultinomialNB()
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.classes_.reshape(1, -1), self.model.predict_proba(X_test) #tuple of dates to prob of dates

    def find_nearest_pred_sale_date_and_prob(self, X_test, today):
        dates, probs = self.predict(X_test) #dates and probs are numpy arrays

        dates_flattened = dates.flatten()
        probs_flattened = probs.flatten()

        min = dates_flattened[0]
        prob = probs_flattened[0]


        for i in range(len(dates_flattened)):
            if abs(today - min) > abs (today - dates_flattened[i]):

                min = dates_flattened[i]
                prob = probs_flattened[i]

        return min, prob


    def add(self, x, y): #adding 1 entry
        self.X_train = np.append(self.X_train, x)
        self.y_train = np.append(self.y_train, y)
        self.model.fit(self.X_train, self.y_train)
