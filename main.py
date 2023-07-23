from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired, URL, ValidationError
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6WlSihBXox7C0sKR6b'
Bootstrap5(app)


def _required(form, field):
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError('Field is required')


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[_required, validators.Length(min=5, message='Too small name')])
    location_url = StringField('Location URL', validators=[DataRequired(message='Please Provide Value'),
                                                           URL(message='Enter Valid URL')])
    open_time = StringField('open time', validators=[DataRequired(message='Please Provide Value')])
    closing_time = StringField('closing time', validators=[DataRequired(message='Please Provide Value')])
    coffee_rating = SelectField('coffee rating', choices=['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'],
                                validators=[DataRequired(message='Please Provide Value')])
    wifi_rating = SelectField('Wifi rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'],
                              validators=[DataRequired(message='Please Provide Value')])
    power_rating = SelectField('Power Outlet Rating', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],
                               validators=[DataRequired(message='Please Provide Value')])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():
        data = [form.cafe_name.data, form.location_url.data, form.open_time.data, form.closing_time.data,
                form.coffee_rating.data, form.wifi_rating.data, form.power_rating.data]
        #print(f"Data is {data}")
        with open('cafe-data.csv', newline='', encoding="utf8", mode='a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)

        return redirect(url_for('cafes'))
    return render_template('add.html',form=form)

        # with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        #     csv_data = csv.reader(csv_file, delimiter=',')
        #     list_of_rows = []
        #     for row in csv_data:
        #         list_of_rows.append(row)




@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
