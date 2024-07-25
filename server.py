from flask import Flask, jsonify, redirect, render_template,request,session
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



@app.route("/sellcar", methods=['POST'])
def sellCar():
    if 'user' in session:
        user_email = session['user']
        user = db.users.find_one({'email': user_email})
        
        if user:
            user_id = user['_id']
            brand = request.form.get('brand')
            variant = request.form.get('variant')
            year = request.form.get('year')
            state = request.form.get('state')
            driven = request.form.get('driven')
            car_pic = request.files.get('carpic')

            car_sale = {
                'user_id': user_id,
                'brand': brand,
                'variant': variant,
                'year': year,
                'state': state,
                'driven': driven
            }

            if car_pic:
                car_pic.save(f'static/uploads/{car_pic.filename}')
                car_sale['carpic'] = car_pic.filename

            db.carsale.insert_one(car_sale)
            return jsonify({'message': 'Car sale added successfully'})
        
    return jsonify({'error': 'User not authenticated'})


@app.route("/fetchcar", methods=['GET'])
def fetchCar():
    if 'user' in session:
        user_email = session['user']
        user = db.users.find_one({'email': user_email})

        if user:
            user_id = user['_id']
            print(f"User ID: {user_id}")  # Debug print to verify user ID

            # Fetch car sales associated with this user
            cars_cursor = db.carsale.find({'user_id': user_id})
            cars = list(cars_cursor)
            print(f"Cars found: {len(cars)}")  # Debug print to verify the number of cars found

            # Convert MongoDB's ObjectId to string for JSON serialization
            for car in cars:
                car['_id'] = str(car['_id'])
                car['user_id'] = str(car['user_id'])

            return jsonify(cars=cars)
        
    # Return empty JSON response if user is not logged in or no cars found
    return jsonify(cars=[])

@app.route("/buycar")
def buycar():
    return render_template('buycar.html')

@app.route("/oldcar")
def oldcar():
    return render_template('oldcars.html')
    
if __name__ == "__main__":
    app.run(debug=True)