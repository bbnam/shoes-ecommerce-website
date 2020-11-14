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
@app.route('/login',methods = ['GET','POST'])
def login():
    # import pdb; pdb.set_trace()
    return render_template('login.html')

@app.route('/check_login', methods = ['GET','POST'])
def check_login():
    name = request.form['name']
    password = request.form['password']

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM user where user_name = %s", (name, ))
    users = cur.fetchall()
    cur.close()
    # import pdb; pdb.set_trace()
    if len(users) > 0 :
        if password == users[0]['password']:
            return jsonify(1)
        return jsonify(0)
    return jsonify(0)
    # return jsonify(users)

@app.route('/shop')
def shop():
    return render_template('category.html')
def get_shoes_image_in_shoes(shoes):
    shoes = [shoes[i]['id'] for i in range(len(shoes))]

    dict = []
    array_image = []
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    for i in shoes:
        cur.execute("select * from shoes where id = %s", (i,))
        shoesid = cur.fetchone()  

        cur.execute("Select name as image from shoes_image where shoes_id =%s", (i,))
        shoes_image = cur.fetchall()

        for image in shoes_image:
            image['image'] = url_for('static', filename=image['image'])
            array_image.append(image['image'])
        shoesid['list_image'] = array_image


        dict.append(shoesid)
        array_image=[]
    cur.close()
    
    return dict
@app.route('/all_shoes')
def all_shoes():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM shoes" )
    shoes = cur.fetchall()
    cur.close()
    shoes = get_shoes_image_in_shoes(shoes)


    return jsonify(shoes)

@app.route('/shop/<id>')  # /landingpageA
def landing_page(id):
    format = request.args.get('format', 'html')
    if format == 'html':
        return render_template('single-product.html')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM shoes where id = %s",(id, ) )
    shoes = cur.fetchall()
    cur.close()

    shoes = get_shoes_image_in_shoes(shoes)
    
    return jsonify(shoes)
if __name__ == "__main__":
	app.run(debug= True)
