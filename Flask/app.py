from flask import Flask, request, render_template, url_for
from utils import get_rating_modelName_salePrice
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/productpage')
def productpage():
    return render_template('productpage.html')


@app.route('/profile')
def profile():
    lst = get_rating_modelName_salePrice()
    return render_template('profile.html', lst=lst)


@app.route('/data', methods=["GET", "POST"])
def data():
    if request.method == 'POST':
        query = request.form['our_params']
        return render_template('data.html', result=query)
    else:
        return render_template('data.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
