from flask import Flask, render_template,request
from pymongo import MongoClient

app=Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"

client = MongoClient('<mongodb_uri>')
db = client.get_database('CarSell')

app.static_folder='static'

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login",methods=['POST','GET'])
def login():
    if(request.method=='POST'):
        email=request.form.get('email')
        password=request.form.get('password')

        print(email,password)
    return render_template('login.html')

@app.route("/register",methods=['POST','GET'])
def register():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        mobile=request.form.get('mobile')
        print(name,email,password,mobile)
    return render_template('register.html')


@app.route("/sellcar")
def sellCar():
    return render_template('sellcar.html')

@app.route("/buycar")
def buycar():
    return render_template('buycar.html')

    
if __name__ == "__main__":
    app.run(debug=True)