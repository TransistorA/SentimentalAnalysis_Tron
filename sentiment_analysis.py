from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import csv
import tweepy

from lxml import html
import requests

# Reference https://towardsdatascience.com/sentiment-analysis-with-python-part-1-5ce197074184


# Define the reg settings
REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")


def preprocess_comments(comments):
    comments = [REPLACE_NO_SPACE.sub("", line.lower()) for line in comments]
    comments = [REPLACE_WITH_SPACE.sub(" ", line) for line in comments]
    return comments


# Transfer the csv file to a txt file
def generate_traindata(csv_file):
    txt_file = "train.txt"
    with open(txt_file, "w") as my_output_file:
        with open(csv_file, "r") as my_input_file:
            [my_output_file.write(" ".join(row) + "\n") for row in csv.reader(my_input_file)]
    my_output_file.close()


def generate_testdata(csv_file):
    txt_file = "test.txt"
    with open(txt_file, "w") as my_output_file:
        with open(csv_file, "r") as my_input_file:
            [my_output_file.write(" ".join(row) + "\n") for row in csv.reader(my_input_file)]
    my_output_file.close()


# Build a classifier and train it with data from twitter
def train():
    generate_traindata("train.csv")

    comments_train = []
    for line in open('train.txt', 'r', encoding='utf-8'):
        if line != "\n":
            comments_train.append(line.strip())

    comments_train_clean = preprocess_comments(comments_train)

    # Vectorization of the train database
    cv = CountVectorizer(binary=True)
    cv.fit(comments_train_clean)
    X = cv.transform(comments_train_clean)

    # Use the nltk library to determine the sentiment of training data, and then use the data to train the classifier.
    sid = SentimentIntensityAnalyzer()
    target = []
    for comment in comments_train_clean:
        ss = sid.polarity_scores(comment)
        if ss["compound"] > 0:
            target.append(1)  # State that the comment is positive
        else:
            target.append(0)  # State that the comment is negative or indifferent

    X_train, X_val, y_train, y_val = train_test_split(X, target, train_size=0.75)

    c_max_accuracy = 0
    for c in [0.01, 0.05, 0.25, 0.5,
              1]:  # the hyperparameter C adjusts the regularization. We need to find the optimal choice of c.
        lr = LogisticRegression(C=c)
        lr.fit(X_train, y_train)
        if accuracy_score(y_val, lr.predict(X_val)) > c_max_accuracy:
            c_optimal = c

    # Generate the final model based on training data
    final_model = LogisticRegression(C=c_optimal)
    final_model.fit(X, target)

    return cv, final_model


# Test the data based on the training model
def test(cv, final_model):
    generate_testdata("test.csv")

    comments_test = []
    for line in open('test.txt', 'r', encoding='utf-8'):
        if line != "\n":
            comments_test.append(line.strip())

    comments_test_clean = preprocess_comments(comments_test)

    # Vectorization of the test database
    X_test = cv.transform(comments_test_clean)
    sentiments = final_model.predict(X_test)
    return sum(sentiments) / len(sentiments)


# A function to make sure that the model works properly by giving the 5 most positive and negative words in dataset
def getPositiveNegativeKeyWords(cv, final_model):
    feature_to_coef = {
        word: coef for word, coef in zip(cv.get_feature_names(), final_model.coef_[0])
    }
    for best_positive in sorted(
            feature_to_coef.items(),
            key=lambda x: x[1],
            reverse=True)[:5]:
        print(best_positive)

    for best_negative in sorted(
            feature_to_coef.items(),
            key=lambda x: x[1])[:5]:
        print(best_negative)


def recommend(sentiment):
    perc = str(sentiment * 100)
    '''gives the basic sentiment analysis'''
    if sentiment < 0.25:
        string = "very negative" + "with" + perc + "% postive tweets"
    if 0.25 < sentiment < 0.5:
        string = "slightly negative " + "with " + perc + "% postive tweets"
    if 0.5 < sentiment < 0.75:
        string = "slightly positive" + "with" + perc + "% postive tweets"
    if 0.75 < sentiment < 0.100:
        string = "very positive " + "with" + perc + "% postive tweets"

    return (string)


def main():
    # This gets the movement of the coin from a simple web scraper
    page = requests.get('https://coinmarketcap.com/currencies/tron/')
    tree = html.fromstring(page.content)
    perDown = tree.xpath('/html/body/div[2]/div/div[1]/div[3]/div[1]/div[1]/span[2]/span/text()')
    movement = perDown[0]

    consumer_key = 'aD0VdJEhOmG27pALUanzBwvuv'
    consumer_secret = 'ovVI2CXSwJ4FayLI7BrusCxQHZje01PEfrbKRmrJ6GYMwh2FZx'
    access_token = '1057247540154900480-604iTbnSXZ5mCK8up01VXZ4vtrj1Rr'
    access_token_secret = 'xpDen6yBtswbAmEhNRqDuCBMXzECmksrbsZxfhPVnmFyR'

    # instantiates API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    cv, model = train()
    sent = test(cv, model)  # gets sentiment
    getPositiveNegativeKeyWords(cv, model) # A function to make sure that the model works properly
    rec = recommend(sent)

    try:
        status = api.update_status("TRX movement is: " + movement + "%" + " and the sentiment is: " + rec)
    except tweepy.error.TweepError:
        pass


main()
