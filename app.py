import re
import nltk
import pickle
import sqlite3 as sql
from nltk.corpus import stopwords
from flask import Flask, render_template, request
from setup import create_schema

create_schema()

nltk.download(["stopwords"])
eng_stopwords = stopwords.words("english")

vectorizer = pickle.load(open('vect.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

sentiment_map = {0: "negative", 1: "postive"}

app = Flask(__name__)

def clean_review(review):
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', review)
    review = re.sub("[^a-zA-Z]", " ",review)
    review = review.lower().split()
    review = [w for w in review if not w in eng_stopwords]
    review = " ".join(review + emoticons)
    return review

@app.route("/")
@app.route("/home.html")
def home():
    return render_template('home.html')

@app.route("/data.html")
def data():
    with sql.connect("predictions.db") as con:
        cur = con.cursor()
        rows = cur.execute("SELECT * FROM results").fetchall()
        return render_template('data.html', results=rows)

@app.route("/result.html", methods=["POST"])
def result():
    if request.method == "POST":
        try:
            review = request.form['review']
            cleaned_review = clean_review(review)
            review_bow = vectorizer.transform([cleaned_review])
            prediction = model.predict(review_bow)[0]
            sentiment = sentiment_map[prediction]
            with sql.connect("predictions.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO results (review, prediction) VALUES (?,?)", (review, sentiment))
                con.commit()
                return render_template('result.html', sentiment=sentiment, movie_id=cur.lastrowid)       
        except:
            return "Oops, something went wrong!", 500

@app.route("/feedback.html", methods=["POST"])
def feedback():
    if request.method == "POST":
        try:
            try:
                feedback = request.form["feedback"]
                feedback = "correct"
            except:
                feedback = "wrong"
            id = request.form["id"]
            with sql.connect("predictions.db") as con:
                cur = con.cursor()
                con.commit()
                cur.execute("UPDATE results SET feedback = ? WHERE id = ?", (feedback, id))
                return render_template('feedback.html')
        except:
            return 'Oops, something went wrong!', 500

if __name__ == "__main__":
    app.run(debug=True)
