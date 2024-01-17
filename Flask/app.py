import secrets
import sqlite3

from flask import Flask, request, render_template, url_for, render_template_string, session, redirect, flash

from werkzeug.security import generate_password_hash, check_password_hash

from Flask.templates.products import products
from Flask.utils.extra import get_characteristic
from Flask.utils.relations import save_favorite_prod, get_recomrndations
from utils.filter import Filter

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/signup', methods=['POST', 'GET'])
def singup():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        filters = Filter()
        if str(password1) == str(password2) and filters.check_email(username):
            # users[username] = generate_password_hash(password2)
            hashed_password = generate_password_hash(password2)
            conn = sqlite3.connect("data/users.sql")
            cursor = conn.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(200), password VARCHAR(200), favorites VARCHAR(1000))')
            cursor.execute(f'INSERT OR REPLACE INTO users (username, password, favorites) VALUES (?, ?, ?)',
                           (username, hashed_password, ""))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
    return render_template("sign_up.html")


@app.route('/logoutprofile')
@app.route('/logoutproductpage')
def logout():
    session.pop('user_id', None)
    flash('You logged out')
    if request.path == "/logoutprofile":
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('productpage'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        filters = Filter()
        if filters.check_email(username):
            conn = sqlite3.connect("data/users.sql")
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username=?', (username,))
            user = cursor.fetchone()
            conn.close()
            if user and check_password_hash(user[0], password):
                session['user_id'] = username
                return redirect(url_for('profile'))
    return render_template("login.html")


@app.route('/productpage')
def productpage():
    username = session.get("user_id")
    login = bool(username)
    lst = get_recomrndations(username)[:3]
    productID = request.args.get('ID')
    productItems, price, itemname = get_characteristic(username, productID)
    return render_template('productpage.html', lst=lst, login=login, productItems=productItems, price=price,
                           itemname=itemname, page_name='productpage')


@app.route('/')
@app.route('/profile', methods=['POST', 'GET'])
def profile():
    # making filters
    filters = Filter()
    all_brandName = list(filters.get_all_for_filtest("brandName") - {None})
    all_shortage = list(filters.get_all_for_filtest("shortage") - {None})
    all_CPU = list(filters.get_all_for_filtest("CPU") - {None})
    all_Display = list(filters.get_all_for_filtest("Display") - {None})
    all_diagonal = list(filters.get_all_for_filtest("diagonal") - {None})
    all_guarantee = list(filters.get_all_for_filtest("guarantee") - {None})
    selected_displays = request.args.getlist('display')
    selected_displays = filters.sets_work(set(selected_displays), set(selected_displays))
    selected_CPU = request.args.getlist('CPU')
    selected_CPU = filters.sets_work(set(selected_CPU), set(all_CPU))

    selected_shortage = request.args.getlist('shortage')
    selected_shortage = filters.sets_work(set(selected_shortage), set(all_shortage))
    selected_guarantee = request.args.getlist('guarantee')
    selected_guarantee = filters.sets_work(set(selected_guarantee), set(all_guarantee))
    selected_diagonal = request.args.getlist('diagonal')
    selected_diagonal = filters.sets_work(set(selected_diagonal), set(all_diagonal))
    selected_brand = request.args.getlist('brand')
    selected_brand = filters.sets_work(set(selected_brand), set(all_brandName))
    lst = filters.get_rating_modelName_salePrice(brandName=selected_brand, shortage=selected_shortage, CPU=selected_CPU,
                                                 Display=selected_displays, diagonal=selected_diagonal,
                                                 guarantee=selected_guarantee)
    search = request.args.get('search')
    if search:
        lst = filters.get_perfect_search(search=search, lst=lst)
        print("final lst : ", lst)
    selected_option = request.form.get('option')
    login1 = bool(session.get("user_id"))
    print(session.get("user_id"))
    if login1:
        id_of_product = request.form.get('like_button')
        if id_of_product:
            save_favorite_prod(id_of_product, session.get("user_id"))
    if selected_option is None:
        return render_template('profile.html',
                               lst=lst,
                               all_brandName=all_brandName,
                               all_shortage=all_shortage,
                               all_CPU=all_CPU,
                               all_Display=all_Display,
                               all_diagonal=all_diagonal,
                               all_guarantee=all_guarantee,
                               login=login1,
                               page_name='profile')
    if selected_option in {"price-increasing", "price-decreasing", "good-rating", "bad-rating", "from-a-to-z",
                           "from-z-to-a"}:
        lst = filters.sort_list_clever(name=selected_option, lst=lst)
        print(lst)
    product_template = products
    return render_template_string(product_template, lst=lst)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
