from flask 	import Flask, render_template, request, flash, url_for,jsonify
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL, MySQLdb
import time
import datetime
import ast

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
            return jsonify(users[0]['id'])
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

@app.route('/size', methods=['POST'])
def all_size_shoes():
    size = request.form['size']
    name = request.form['name']
    # import pdb; pdb.set_trace()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id, amount FROM specific_shoes where shoes_id = %s and name = %s",(size,name, ) )
    size_shoes = cur.fetchall()
    cur.close()

    return jsonify(size_shoes)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/order', methods=['POST'])
def order():
    order = request.form['order']
    address = request.form['address']
    order_city = request.form['city']
    user_id = request.form['user']
    
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    order = ast.literal_eval(order)
         
    state = 'active'

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("SELECT id FROM `order` ")
    all_order = cur.fetchall()
    id_order = len(all_order) + 1

    query = '''
        INSERT INTO `order`(id, create_time, user_id, address, city, state) 
        VALUES ({}, '{}', {}, '{}', '{}', '{}')
    '''.format(id_order, create_time, user_id, address, order_city, state)
 
    cur.execute(query)
    mysql.connection.commit()



    for i in range(len(order)):
        key = order[i].get('key').split(' - ')

        query = '''
        INSERT INTO `order_has_size`(order_id, size_id, quantity) 
        VALUES ({}, {}, {})
        '''.format(id_order, key[5], order[i].get('value'))
        
        cur.execute(query)
        mysql.connection.commit()
        

        cur.execute("SELECT amount FROM specific_shoes where id = %s",(key[5], ) )
        amount = cur.fetchall()


        new_amount = amount[0].get('amount') - order[i].get('value')

        cur.execute("UPDATE specific_shoes SET amount = %s WHERE id = %s", (new_amount, key[5] ))
        mysql.connection.commit()

        
    cur.close()

    return jsonify('1')



@app.route('/confirmation')
def confrim():
    return render_template('confirmation.html')

@app.route('/showorder', methods=['POST'])
def showorder():
    user_id = request.form['user_id']

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = '''
    select id, address, city from `order`
    where state = 'active' and user_id = {}
    '''.format(user_id)
    cur.execute(query)
    all_order = cur.fetchall()

    # order = ast.literal_eval(all_order)
    
    for order in all_order:
        order_id = order.get('id')
        query = '''
        SELECT specific_shoes.name, order_has_size.quantity, shoes.name as sh,  order_has_size.quantity* shoes.price as total
        FROM specific_shoes
        INNER JOIN shoes ON shoes.id=specific_shoes.shoes_id
        INNER JOIN order_has_size ON order_has_size.size_id=specific_shoes.id
        where order_has_size.order_id = {}
        '''.format(order_id)
        cur.execute(query)
        shoes = cur.fetchall()


        order['shoes'] = shoes
 
    # import pdb;pdb.set_trace()
    cur.close()


    return jsonify(all_order)
if __name__ == "__main__":
	app.run(debug= True)
