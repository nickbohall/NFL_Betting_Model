from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
import numpy as np
import seaborn as sns

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker


def logistic_regression(df):
    # ------------------------------------ SET UP FOR MODELING ------------------------------------#

    target = 'home_team_win'
    features = [column for column in df.columns if 'ewma' in column and 'dynamic' in column]
    for feature in features:
        print(feature)

    df = df.dropna()

    X = df.loc[df['season'] != 2020, features].values
    y = df.loc[df['season'] != 2020, target].values

    # ------------------------------------ MODEL THE DATA ------------------------------------#

    clf = LogisticRegression()
    clf.fit(X, y)

    accuracy_scores = cross_val_score(clf, X, y, cv=10)
    log_losses = cross_val_score(clf, X, y, cv=10, scoring='neg_log_loss')

    print('Model Accuracy:', np.mean(accuracy_scores))
    print('Neg log loss:', np.mean(log_losses))

    fig, ax = plt.subplots()

    feature_names = ['_'.join(feature_name.split('_')[3:]) for feature_name in features]

    coef_ = clf.coef_[0]

    features_coef_sorted = sorted(zip(feature_names, coef_), key=lambda x: x[-1], reverse=True)

    features_sorted = [feature for feature, _ in features_coef_sorted]
    coef_sorted = [coef for _, coef in features_coef_sorted]

    ax.set_title('Feature importance')

    ax.barh(features_sorted, coef_sorted)
    plt.show()

    # ------------------------------------ PREDICTIONS ------------------------------------#

    df_2020 = df.loc[(df['season'] == 2020)].assign(
        predicted_winner=lambda x: clf.predict(x[features]),
        home_team_win_probability=lambda x: clf.predict_proba(x[features])[:, 1]
    ) \
        [['home_team', 'away_team', 'week', 'predicted_winner', 'home_team_win_probability', 'home_team_win']]

    df_2020['actual_winner'] = df_2020.apply(lambda x: x.home_team if x.home_team_win else x.away_team, axis=1)
    df_2020['predicted_winner'] = df_2020.apply(lambda x: x.home_team if x.predicted_winner == 1 else x.away_team, axis=1)
    df_2020['win_probability'] = df_2020.apply(
        lambda x: x.home_team_win_probability if x.predicted_winner == x.home_team else 1 - x.home_team_win_probability,
        axis=1)
    df_2020['correct_prediction'] = (df_2020['predicted_winner'] == df_2020['actual_winner']).astype(int)

    df_2020 = df_2020.drop(columns=['home_team_win_probability', 'home_team_win'])

    print(df_2020.sort_values(by='win_probability', ascending=False).reset_index(drop=True).head(10))

def linear_regression(df):

    # ------------------------------------ SET UP FOR MODELING ------------------------------------#

    df = df.dropna()
    target = df['score_diff']
    feature_cols = [column for column in df.columns if 'ewma' in column and 'dynamic' in column]
    features = df[feature_cols]

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=10)
    print(X_train.shape, y_train.shape)

    # ------------------------------------ MODEL THE DATA ------------------------------------#

    clf = LinearRegression()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    regr_coef = pd.DataFrame(data=clf.coef_, index=X_train.columns, columns=['Coefficient'])
    residuals = (y_train - y_pred)
    trend = np.polyval(clf,y_test)

    print(f"Coefficients: {regr_coef}")
    print(f"Intercept: {clf.intercept_ : .3f}")
    print(f"MSE: {mean_squared_error(y_test, y_pred): .3f} ")
    print(f"Coefficient of determination (R^2): {r2_score(y_test, y_pred): .3f}")

    plt.figure(figsize=(15, 10))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title("Actual vs. Predicted")
    plt.plot(y_test, trend)
    plt.show()

class LinearRegressionTest():
    def __init__(self, lr = 0.001, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0


        for _ in range(self.n_iters):
            y_pred = np.dot(X, self.weights) + self.bias

            dw = (1/n_samples) * np.dot(X.T, (y_pred -y))
            db = (1/n_samples) * np.sum(y_pred-y)

            self.weights = self.weights - self.lr * dw
            self.bias = self.bias - self.lr * db

    def predict(self, X):
        y_pred = np.dot(X, self.weights) + self.bias
        return y_pred

