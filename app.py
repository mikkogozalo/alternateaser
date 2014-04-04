from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from pymongo import MongoClient
import pyteaser
import os

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = MongoClient().alternateaser

@app.route('/', methods = ['GET'])
def index():
    return render_template('home.html', route='about')

@app.route('/tease', methods = ['POST'])
def tease():
    if request.form is None or 'url' not in request.form or request.form['url'] == '':
        return jsonify({'status': 'error', 'message': 'Please enter a valid URL.'}), 200
    article = pyteaser.grab_link(request.form['url'])
    if article is None or article.cleaned_text == "":
        return jsonify({'status': 'error', 'message': 'Sorry, I can\'t summarize that website. :('}), 200
    
    entry = {}
    entry['slug'] = os.urandom(3).encode('hex')
    entry['title'] = str(article.title.encode('utf-8', 'ignore'))
    text = str(article.cleaned_text.encode('utf-8', 'ignore'))
    entry['summary'] = pyteaser.Summarize(entry['title'], text)
    db.article.insert(entry)
    return jsonify({'status': 'redirect', 'message': url_for('article', slug = entry['slug'])}), 200

@app.route('/s/<slug>')
def article(slug):
    article = db.article.find_one({"slug": slug})
    if article is None:
        flash("Sorry, the article you specified does not exist", "danger")
        return redirect(url_for('index'))
    return render_template('article.html', title=article['title'], article=article)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')