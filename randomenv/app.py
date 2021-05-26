from flask import render_template
from flask import Flask,redirect
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm.exc import UnmappedClassError, UnmappedInstanceError
import sys
import requests
from flask import request,flash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)



class city(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50),unique=True, nullable=False )
    city_temperature = db.Column(db.String(50), nullable=False)
    city_state = db.Column(db.String(50), nullable=False)
    TimeNoted = db.Column(db.String(50), nullable=False)
    pat = db.Column(db.String(15), nullable=False)
    present_time=db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<City %r>'%self.city_name


#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')

    #render_template('index.html', weather=city_weather)

# @app.route('/delete_city', methods=['GET', 'POST'])
# def delete_city():
#     #del_city = city.query.filter_by(city_name=request.form['tobedeleted']).first()
#     #return str(request.form['tobedeleted'])
#     del_city = city.query.filter_by(city_name=request.form['tobedeleted']).first()
#     db.session.delete(del_city)
#     db.session.commit()
#     return redirect('/')
@app.route('/delete_city/<city_id>', methods=['GET', 'POST'])
def delete_city(city_id):
    #del_city = city.query.filter_by(city_name=request.form['tobedeleted']).first()
    #return str(request.form['tobedeleted'])
    del_city = city.query.filter_by(id=city_id).first()
    db.session.delete(del_city)
    db.session.commit()
    return redirect('/')



@app.route('/',methods=['GET','POST'])
def index():
    error = None
    city_name = None
    city_weather = None
    open_weather_api = '52fa4e1decd455f1fb5d606852318947'
    time_api='uqdgVpGRG38uAVG58xQGjKd2ERgzyw'
    if request.method == 'POST':
        city_name = str(request.form['city_name'])
        print(city_name)
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'.format(city_name, open_weather_api))
        t = requests.get('https://www.amdoren.com/api/timezone.php?api_key={0}&loc={1}'.format(time_api,city_name ))
        if r:
            weather_value = r.json()
            celsius = float((int(weather_value['main']['temp']))) - 273.15
            celsius = round(celsius,1)
            time_details=t.json()
            present_datetime=time_details["time"]
            #create dictionary to hold and pass data to html properly
            city_weather = {
                'city_name': city_name.upper(),
                'temp': str(celsius),
                'main': weather_value['weather'][0]['main']
            }
            timestamp=datetime.utcfromtimestamp(int(weather_value["dt"])).strftime('%H:%M:%S %d-%m-%Y')
            tag = int(present_datetime[11:13])
            pat = ""
            if tag<=12:
                pat += "day"
            elif tag<=18:
                pat += "evening-morning"
            elif tag<=23:
                pat += "night"

            exists = city.query.filter_by(city_name=city_weather['city_name']).first()
            if not exists:
                city_variable = city(city_name=city_weather['city_name'],city_state=city_weather['main'],city_temperature=city_weather['temp'],
                                     TimeNoted=timestamp , pat = pat,present_time=present_datetime)
                db.session.add(city_variable)
                db.session.commit()
            else:
                #update the enty if exists
                flash("The city already added , entry updated !! ")
                exists.city_temperature=city_weather['temp']
                exists.city_state=city_weather['main']
                exists.TimeNoted=(timestamp)
                exists.pat = pat
                exists.present_time=present_datetime
                db.session.commit()

        else:
            flash("The city doesn't exist!")
        #return city_weather
    # fresh_list=[]
    # for item in list(city.query.all()):
    #     temp=list(map(str,item.split()))
    #     dictionary={}
    #     dictionary['temp']=temp[1]
    #     dictionary['state']=temp[2]
    #     dictionary['city_name']=temp[0]
    #     fresh_list.append(dictionary)
    #
    # fresh_dictionary={"weathers":fresh_list}
    our_citys=city.query.order_by(city.id)
    return render_template('index.html', our_citys=our_citys)
     #redirect(url_for('index'))
    #return render_template('index.html', weather=city_weather)

# @app.route('/add',methods=['GET','POST'])
#
# def addcity():
#     # city_name = request.form.get('city_name')
#     # r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city_name+'&appid=52fa4e1decd455f1fb5d606852318947')
#     # dict_with_weather_info = r.json()
#     #return dict_with_weather_info['main']
#     error = None
#     city_name = None
#     city_weather = None
#     open_weather_api = '52fa4e1decd455f1fb5d606852318947'
#     if request.method == 'POST':
#         city_name = str(request.form['city_name']).replace(' ', '')
#         print(city_name)
#         r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'.format(city_name, open_weather_api))
#         if r:
#             weather_value = r.json()
#             # celsius = int(pytemperature.k2c(int(weather_value['main']['temp'])))
#             celsius = float((int(weather_value['main']['temp']))) - 273.15
#             celsius = round(celsius,2)
#             city_weather = {
#                 'city_name': city_name.upper(),
#                 'temp': str(celsius),
#                 'main': weather_value['weather'][0]['main']
#             }
#         else:
#             pass
#
#     return render_template('add.html', weather=city_weather)
    # return render_template('index.html', weather=dict_with_weather_info['main'])
    #return render_template('index.html',weather=dict_with_weather_info)




# don't change the following way to run flask:
if __name__ == '__main__':
    #db.drop_all()
    db.create_all()
    app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True,port=5000,threaded=True)


    #
    # if len(sys.argv) > 1:
    #     arg_host, arg_port = sys.argv[1].split(':')
    #     app.run(host=arg_host, port=arg_port)
    # else:
    #     app.run()
