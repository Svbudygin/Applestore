products = """
            {% for product in lst %}
                <div class="col-md-6 col-sm-8">
                    <div class="small-box-c">
                        <div class="small-img-b">
                            <a href="/productpage?ID={{product['productId']}}"><img
                                    src="../static/images/tr1.png"
                                    alt="#"/></a>
                        </div>
                        <div class="dit-t clearfix">
                            <div class="left-ti">
                                <p>{{product["modelName"]}}</p>
                            </div>
                            <a href="/productpage" tabindex="0">{{product["salePrice"]}}₽</a>
                        </div>
                        <form action="{{url_for('profile')}}" method="post">
                            <div class="prod-btn">
                                <a href="#"><i class="fa fa-star"
                                               aria-hidden="true"></i>
                                    {{product['rating']}}</a>
                                <button type="submit" name="like_button"
                                        value="{{ product['productId'] }}">
                                    <i class="fa fa-thumbs-up" aria-hidden="true"></i>Like
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
                {% endfor %}
        """