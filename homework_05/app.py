"""
Домашнее задание №5
Первое веб-приложение

создайте базовое приложение на Flask
создайте index view /
добавьте страницу /about/, добавьте туда текст
создайте базовый шаблон (используйте https://getbootstrap.com/docs/5.0/getting-started/introduction/#starter-template)
в базовый шаблон подключите статику Bootstrap 5 и добавьте стили, примените их
в базовый шаблон добавьте навигационную панель nav (https://getbootstrap.com/docs/5.0/components/navbar/)
в навигационную панель добавьте ссылки на главную страницу / и на страницу /about/ при помощи url_for
"""

from flask import Flask, request, render_template
from homework_05.views.products import product_app

app = Flask(__name__)

app.register_blueprint(product_app, url_prefix="/products")


@app.route("/")
def hello_index():
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def delivery_of_products():
    print(request.environ)
    if request.method == "GET":
        return "Доставка  продуктов"

    name = request.form.get("name")
    return f"Доставка  {name}!"


@app.route("/Delivery/")
@app.route("/Delivery/<name>/")
def delivery(name="Продуктов"):
    return f"Доставка {name}!"


@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
