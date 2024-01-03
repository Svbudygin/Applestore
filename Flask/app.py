from datetime import datetime

from flask import Flask, request, render_template, url_for, render_template_string
from utils.filter import Filter

app = Flask(__name__)


@app.route('/productpage')
def productpage():
    return render_template('productpage.html')


@app.route('/')
@app.route('/profile', methods=['POST', 'GET'])
def profile():
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
    print(request.args.get('option'),
          filters.get_rating_modelName_salePrice(brandName=selected_brand, shortage=selected_shortage, CPU=selected_CPU,
                                                 Display=selected_displays, diagonal=selected_diagonal,
                                                 guarantee=selected_guarantee))
    lst = filters.get_rating_modelName_salePrice(brandName=selected_brand, shortage=selected_shortage, CPU=selected_CPU, Display=selected_displays, diagonal=selected_diagonal,
                                                 guarantee=selected_guarantee)
    selected_option = request.form.get('option')
    if selected_option is None:
        return render_template('profile.html',
                               lst=lst,
                               all_brandName=all_brandName,
                               all_shortage=all_shortage,
                               all_CPU=all_CPU,
                               all_Display=all_Display,
                               all_diagonal=all_diagonal,
                               all_guarantee=all_guarantee,
                               )
    if selected_option in {"price-increasing", "price-decreasing", "good-rating", "bad-rating", "from-a-to-z",
                           "from-z-to-a"}:
        lst = filters.sort_list_clever(name=selected_option, lst=lst)
    print(selected_option)
    product_template = """
            {% for product in lst %}
                                                <div class="col-md-6 col-sm-8">
                                                    <div class="small-box-c">
                                                        <div class="small-img-b">
                                                            <a href="/productpage"><img src="../static/images/tr1.png" alt="#"/></a>
                                                        </div>
                                                        <div class="dit-t clearfix">
                                                            <div class="left-ti">
                                                                <p>{{product[1]}}</p>
                                                            </div>
                                                            <a href="/productpage" tabindex="0">{{product[2]}}₽</a>
                                                        </div>
                                                        <div class="prod-btn">
                                                            <a href="/productpage"><i class="fa fa-star" aria-hidden="true"></i>
                                                                {{product[0]}}</a>
                                                            <a href="/productpage"><i class="fa fa-thumbs-up"
                                                                           aria-hidden="true"></i>Like</a>
                                                        </div>
                                                    </div>
                                                </div>
                                                {% endfor %}
        """
    return render_template_string(product_template, lst=lst)


@app.route('/data', methods=["GET", "POST"])
def data():
    if request.method == 'POST':
        query = request.form['our_params']
        return render_template('data.html', result=query)
    else:
        return render_template('data.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
