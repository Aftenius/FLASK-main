from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro_text = db.Column(db.String(300), nullable=False)
    main_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.Integer)

    def __repr__(self):
        return '<Frticle %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    product = Shop.query.order_by(Shop.id).all()
    return render_template("index.html", product=product)


@app.route('/sign')
def sign_in():
    return render_template("sign.html")


@app.route('/create', methods=['POST', 'GET'])
def create_post():
    if request.method == "POST":
        title = request.form['title']
        intro_text = request.form['intro_text']
        main_text = request.form['main_text']

        product = Shop(title=title, intro_text=intro_text, main_text=main_text)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return "произошла ошибка"
    else:
        return render_template("create.html")


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f'User: {name}, id: {id}'


if __name__ == '__main__':
    app.run(debug=True)