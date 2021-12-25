from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class NewCafeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    sockets = SelectField("Has Sockets?", choices=[(1, 'Yes'), (0, "No")], validators=[DataRequired()])
    toilet = SelectField("Has Toilet?", choices=[(1, 'Yes'), (0, "No")], validators=[DataRequired()])
    wifi = SelectField("Has WiFi?", choices=[(1, 'Yes'), (0, "No")], validators=[DataRequired()])
    call = SelectField("Can Take Calls?", choices=[(1, 'Yes'), (0, "No")], validators=[DataRequired()])
    submit = SubmitField("Submit")


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    has_sockets = db.Column(db.Integer)
    has_toilet = db.Column(db.Integer)
    has_wifi = db.Column(db.Integer)
    can_take_calls = db.Column(db.Integer)
    seats = db.Column(db.String)
    coffee_price = db.Column(db.String)
    map_url=db.Column(db.String)
    img_url=db.Column(db.String)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('sockets') == 'checked':
            a = [1]
        else:
            a = [1, 0]
        if request.form.get('toilet') == 'checked':
            b = [1]
        else:
            b = [1, 0]
        if request.form.get('wifi') == 'checked':
            c = [1]
        else:
            c = [1, 0]
        if request.form.get('call') == 'checked':
            d = [1]
        else:
            d = [1, 0]
        filtered_cafes = Cafe.query.filter(Cafe.has_sockets.in_(a), Cafe.has_toilet.in_(b),Cafe.has_wifi.in_(c),Cafe.can_take_calls.in_(d)).all()
        return render_template('index.html', all_cafes=filtered_cafes)
    else:
        all_cafes = Cafe.query.all()
        return render_template('index.html', all_cafes=all_cafes)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = NewCafeForm()
    if form.validate_on_submit():
        name=form.name.data
        sockets=form.sockets.data
        toilet=form.toilet.data
        wifi=form.wifi.data
        call=form.call.data
        new_cafe = Cafe(name=name, has_sockets=sockets, has_toilet=toilet, has_wifi=wifi, can_take_calls=call, location="N/A", seats="N/A", coffee_price="N/A", map_url="N/A", img_url="N/A")
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)