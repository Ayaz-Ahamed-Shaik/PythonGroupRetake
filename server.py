from flask import Flask, redirect, render_template,request,session
from pymongo import MongoClient

app=Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://ayaz55ahammad:ayaz%401234@cluster0.ega3cqv.mongodb.net/"

client = MongoClient(app.config['MONGO_URI'])
db = client.get_database('CarSell')

app.static_folder='static'

app.secret_key='1234'
@app.route("/")
def home():
    if(session.get('user')):
       print('user',session.get('user'))
       return render_template('index.html',username=session.get('user'))
    return render_template('index.html',username="")

@app.route("/login",methods=['POST','GET'])
def login():
    if(request.method=='POST'):
        email=request.form.get('email')
        password=request.form.get('password')
        message=''
        if(email==''):
            message='email cannot be empty!'
        if(password==''):
            message='password cannot be empty!'  

        if(message):    
            return redirect('/login')  
        
        else:
            user=db.users.find_one({"email":email})
            if(user):
                 if(user['password']==password):
                     session['user']=str(email)
                     return redirect('/')   
                 else:
                    return render_template('login.html',message="Wrong password")
       
    return render_template('login.html',message="Kindly register yourself!")

@app.route("/logout")
def logout():
    if(session.get('user')):
       session.pop('user', None)
       return render_template('index.html',username="")


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

        if(message):    
            return render_template('register.html',message= message)  
        
        else:
            user=db.users.find_one({"email":email})
            if(user):
                 return render_template('register.html',message="User already registered!")   
            db.users.insert_one({"name":name,"email":email,"password":password,"mobile":mobile})
    return render_template('register.html',message="User successfully registered!Kindly Login!")
 
@app.route("/sell_car", methods=['GET', 'POST'])
def sell_Car():
       if(session.get('user')):
           return render_template('sellcar.html',username=session.get('user'))
       return render_template('sellcar.html',username="")


@app.route("/sellcar", methods=['GET', 'POST'])
def sellCar():
    if request.method == 'POST':
        mode = request.form.get('mode')
        brand = request.form.get('brand')
        variant = request.form.get('variant')
        year = request.form.get('year')
        state = request.form.get('state')
        driven = request.form.get('driven')
        carFile = request.files.get('carpic')  
        
        if(mode==''):
            return render_template('sellcar.html',message="mode empty!")
        if(brand==''):
            return render_template('sellcar.html',message="brand empty!")
        if(variant==''):
            return render_template('sellcar.html',message="variant empty!")
        if(year==''):
            return render_template('sellcar.html',message="year empty!")
        if(state==''):
            return render_template('sellcar.html',message="state empty!")
        if(driven==''):
            return render_template('sellcar.html',message="driven empty!")
        if carFile and carFile.filename:
            file_path = f'static/uploads/{carFile.filename}' 
            carFile.save(file_path)
            if(session.get('user')):
                db.carsale.insert_one({"mode":mode,"brand":brand,"variant":variant,"year":year,"state":state,"driven":driven})
                return render_template('sellcar.html',message="Details Saved succesfully!")
            else:
                return render_template('sellcar.html',message="Kindly Login!")  
        else:
            return render_template('sellcar.html',message="No car image!")
            
    return render_template('sellcar.html')

@app.route("/buycar")
def buycar():
    return render_template('buycar.html')

    
if __name__ == "__main__":
    app.run(debug=True)