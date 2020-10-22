from flask 	import Flask, render_template, request, flash, url_for,jsonify
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_DB'] = 'mydb'

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/check_login', methods = ['POST'])
def check_login():
   
    name = request.form['name']
    password = request.form['password']
    import pdb; pdb.set_trace()
    return 'hi'
if __name__ == "__main__":
	app.run(debug= True)
