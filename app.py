from flask import Flask, render_template, request, redirect, flash
from sqlalchemy.exc import IntegrityError
import sys
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse
import secrets

app = Flask(__name__)
db = SQLAlchemy(app)
get_parser = reqparse.RequestParser()
secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather1.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = secret_key


class City(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    city_name = db.Column(db.String(80), unique=True, nullable=False)
    state = db.Column(db.String(80), unique=False, nullable=False)
    temp = db.Column(db.String(4), unique=False, nullable=False)
    time_image = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '{}'.format(self.city_name)


db.create_all()


def day_or_night(current_time, sunrise_time, sunset_time):
    if int(current_time) < int(sunrise_time):
        return "evening-morning"
    elif int(current_time) < int(sunset_time):
        return "day"
    else:
        return "night"


@app.route('/')
def index():
    return render_template("index.html", data=City.query.all())


@app.route('/add', methods=['GET', 'POST'])
def add_city():
    get_user_city_name = ''.join(request.form.getlist('city_name'))
    if get_user_city_name == '':
        flash("You must enter a city name!")
        return redirect('/')
    else:
        pass
    try:
        api_key = 'f4f61fa3eeb5ccac21d8d8be41928bcb'
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(get_user_city_name, api_key)
        r = requests.get(url)
        city_info_test = City(city_name=str(json.loads(r.content)["name"]),
                              state=str(
                                  {k: v for e in json.loads(r.content)["weather"] for (k, v) in
                                   e.items()}.get("main")),
                              temp=str(
                                  int(json.loads(r.content)["main"].get("temp") - 273.15)),
                              time_image=str(day_or_night(json.loads(r.content)['dt'], json.loads(r.content)['sys']
                                                          .get('sunrise'), json.loads(r.content)['sys'].get('sunset'))))
        db.session.add(city_info_test)
        db.session.add(city_info_test)
        db.session.commit()
        return redirect('/')
    except IntegrityError:
        flash("The city has already been added to the list!")
        return redirect('/')
    except KeyError:
        flash("The city doesn't exist!")
        return redirect('/')


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(city_name=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


# don't change the following way to run flask:
# if __name__ == '__main__':
#     db.drop_all()
#     db.create_all()
#     app.secret_key = 'super secret key'
#     #app.config['SESSION_TYPE'] = 'filesystem'
#     app.run(debug=True,port=8000)
if __name__ == '__main__':
<<<<<<< HEAD
=======
    db.drop_all()
    db.create_all()
    app.secret_key = 'super secret key'
>>>>>>> fe5eb36efe4495422827af7ceee406709b7d01cd
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
<<<<<<< HEAD
        app.run()
=======
        app.run(debug=True)
    #
    # if len(sys.argv) > 1:
    #     arg_host, arg_port = sys.argv[1].split(':')
    #     app.run(host=arg_host, port=arg_port)
    # else:
    #     app.run()
>>>>>>> fe5eb36efe4495422827af7ceee406709b7d01cd
