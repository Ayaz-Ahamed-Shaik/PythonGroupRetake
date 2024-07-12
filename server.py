from flask import Flask, render_template

app=Flask(__name__)


app.static_folder='static'

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/sellcar")
def sellCar():
    return render_template('sellcar.html')

@app.route("/buycar")
def buycar():
    return render_template('buycar.html')

    
if __name__ == "__main__":
    app.run(debug=True)