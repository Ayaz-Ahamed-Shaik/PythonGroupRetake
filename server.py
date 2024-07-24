from flask import Flask, render_template,request,session
from pymongo import MongoClient

app=Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://ayaz55ahammad:ayaz%401234@cluster0.ega3cqv.mongodb.net/"

client = MongoClient(app.config['MONGO_URI'])
db = client.get_database('CarSell')

app.static_folder='static'

app.secret_key='1234'
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
        message=''
        if(name==''):
            message='Name cannot be empty!'
        if(email==''):
            message='email cannot be empty!'
        if(password==''):
            message='password cannot be empty!'
        if(mobile==''):
            message='mobile cannot be empty!'    
            
        return render_template('register.html',message= message)  
    return render_template('register.html',message="")
 

@app.route("/sellcar")
def sellCar():
    return render_template('sellcar.html')

@app.route("/buycar")
def buycar():
    return render_template('buycar.html')

    
if __name__ == "__main__":
    app.run(debug=True)