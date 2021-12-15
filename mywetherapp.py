# 'api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=858e733be4ec10f41d137b722d6957ec'
from datetime import datetime
from enum import unique
from flask import Flask,render_template,request
from flask import Flask, render_template ,url_for , request , redirect
import os, requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table_data.db'
db = SQLAlchemy(app)

class wetherdata(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    city = db.Column(db.Text, nullable=False,unique=True)
    country = db.Column(db.Text, nullable=False)
    temp = db.Column(db.Text, nullable=False)
    temp_min = db.Column(db.Text, nullable=False)
    temp_max = db.Column(db.Text, nullable=False)
    speed = db.Column(db.Text, nullable=False)
    humidity = db.Column(db.Text, nullable=False)
    # location = db.Column(db.Text, nullable=False)
    # Timing = db.Column(db.Text, nullable=False)
    Timing = db.Column(db.DateTime(timezone=True), default=datetime.now())

    def __repr__(self):
        return "Wether  POST "+ str(self.city)
# app = Flask(__name__)
@app.route('/new_d/<name>')
def new(name):
    return name
@app.route('/', methods =['GET','POST'])
def new_d():
    if request.method=='POST':
        text=request.form['text']
        prossed_text=text.capitalize()
        construct_url = "https://api.openweathermap.org/data/2.5/weather?q="+prossed_text+"&APPID=858e733be4ec10f41d137b722d6957ec"
        response = requests.get(construct_url)
        list_of_data = response.json()
        # data=[list_of_data]
        db.create_all()
        exists = db.session.query(wetherdata.city).filter_by(city=prossed_text).first() is not None
        if exists:
            cities=wetherdata.query.order_by(wetherdata.city).limit(5).all()
            all_post=wetherdata.query.filter_by(city=prossed_text).first()
            all_post=[all_post]
            return render_template('my_new.html',data=all_post,data3=cities)
        else:
            db.create_all()
            new_post = wetherdata(city =prossed_text,country=str(list_of_data['sys']['country']),temp=str(list_of_data['main']['temp']) + 'k',temp_min=str(list_of_data['main']['temp_min']) + 'k',temp_max=str(list_of_data['main']['temp_max']) + 'k',speed=str(list_of_data['wind']['speed']),humidity=str(list_of_data['main']['humidity']))
            # print(new_post)
            db.session.add(new_post)
            db.session.commit()
            cities=wetherdata.query.order_by(wetherdata.city).limit(5).all()
            all_post=wetherdata.query.filter_by(city=prossed_text).first()
            all_post=[all_post]
            return render_template('my_new.html',data=all_post,data3=cities)
        # return redirect('/')
    else:
        return render_template('my_new.html')
        # return render_template('my_new.html')
if __name__ == "__main__":
    app.run(debug=True)