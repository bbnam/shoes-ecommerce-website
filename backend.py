from flask 	import Flask, render_template, redirect, request, flash, url_for,jsonify, session, send_from_directory,render_template
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL, MySQLdb
import time
import datetime
import ast
from authy.api import AuthyApiClient
from random import randint
from textmagic.rest import TextmagicRestClient
from sendmail import send_mail, random_code
from flask_mail import Mail, Message 
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath





app = Flask(__name__)
mysql = MySQL(app)



UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/avatar/')
UPLOADS_IMG = join(dirname(realpath(__file__)), 'static/product/')


app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_DB'] = 'mydb'



app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bbnam159@gmail.com'
app.config['MAIL_PASSWORD'] = 'haiduong123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



# UPLOAD_FOLDER = 'home/desktop/'




app.config['AVATAR'] = UPLOADS_PATH
app.config['PRODUCT'] = UPLOADS_IMG
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login',methods = ['GET','POST'])
def login():
    # import pdb; pdb.set_trace()
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

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

        cur.execute("Select name as image, index_image from shoes_image where shoes_id =%s and index_image != '0' ORDER BY index_image ASC", (i,))
        shoes_image = cur.fetchall()

        for image in shoes_image:
            image['image'] = url_for('static', filename=image['image'])
            array_image.append(image)
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



@app.route('/add-comment', methods=['POST'])
def add_cmt():
    rate = request.form['rate']
    comment = request.form['comment']
    shoes_id = request.form['shoes_id']
    user_id = request.form['user_id']

    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query ='''
    INSERT INTO `mydb`.`comment` 
    (`create_time`, `comment`, `user_id`, `shoes_id`, `rate`) 
    VALUES ('{}', '{}', {}, {}, {});
    '''.format(create_time, comment, user_id, shoes_id, rate)


    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    mysql.connection.commit()
    cur.execute('Select user_name from user where id = %s', (user_id, ))
    user_name = cur.fetchone()
    cur.close()

    return jsonify(user_name)
    


@app.route('/shop/<name>')  # /landingpageA
def landing_page(name):
    format = request.args.get('format', 'html')
    id = name[-1]
    # import pdb; pdb.set_trace()
    if format == 'html':
        return render_template('single-product.html')

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM shoes where id = %s",(id, ) )
    shoes = cur.fetchall()
    cur.close()

    shoes = get_shoes_image_in_shoes(shoes)
    
    return jsonify(shoes)


@app.route('/get-single-review',methods=['POST'])
def get_single_review():
    shoes_id = request.form['shoes_id']
    user_id = request.form['user_id']

    query = '''
        select user.name, user.avatar, comment.rate, comment.comment
        from user 
        INNER JOIN comment
        ON comment.user_id = user.id
        where comment.user_id ={} and comment.shoes_id = {}
    '''.format(user_id, shoes_id)

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    comment = cur.fetchall()
    cur.close()
    comment[0]['avatar'] = url_for('static', filename=comment[0]['avatar'])
    
    
    return jsonify(comment)



@app.route('/get-all-review', methods=['POST'])
def get_all_review():
    shoes_id = request.form['shoes_id']
    query = '''
        select user.name, user.avatar, comment.rate, comment.comment
        from user 
        INNER JOIN comment
        ON comment.user_id = user.id
        where comment.shoes_id = {}
    '''.format( shoes_id)

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    comment = cur.fetchall()
    cur.close()

    for image in comment:
        image['avatar'] = url_for('static', filename=image['avatar'])
            

    return jsonify(comment)





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


@app.route('/shoes-id', methods=['POST'])
def shoes_id():
    id = request.form['id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM shoes where id = %s",(id, ) )
    shoes = cur.fetchall()
    cur.close()

    shoes = get_shoes_image_in_shoes(shoes)
    return jsonify(shoes)

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

@app.route('/show_all_order', methods=['GET'])
def show_all_order():

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = '''
    select id, address, city from `order`
    where state = 'active'
    '''
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

@app.route('/categories', methods=['GET'])
def categories():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM categories" )
    categories = cur.fetchall()
    cur.close()
    return jsonify(categories)


@app.route('/category', methods=['POST'])
def category():
    name = request.form['id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)



    cur.execute("SELECT * FROM shoes where categories_id = %s",(name) )
    shoes = cur.fetchall()
    cur.close()
    shoes = get_shoes_image_in_shoes(shoes)

    return jsonify(shoes)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    # import pdb; pdb.set_trace()
    file = request.files['image']
    id = request.cookies.get('user')
    

    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            link = os.path.join(app.config['AVATAR'], filename).replace('/home/nam/Desktop/Web/static/',"")
            query = '''
            UPDATE `mydb`.`user` SET `avatar`='{}' WHERE `id`={};


            '''.format(link, id)
            # import pdb; pdb.set_trace()

            # import pdb; pdb.set_trace()

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            mysql.connection.commit()
            cur.close()
            file.save(os.path.join(app.config['AVATAR'], filename))
            return redirect(url_for('profile'))


    return "ooooooppppppssss"

@app.route('/upload-name', methods=['POST'])
def upload_name():
    id = request.form['id']
    name = request.form['name'].encode('utf-8')

    query = '''
    UPDATE `mydb`.`user` SET `name`='{}' WHERE `id`={};

    '''.format(name, id)
  

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    mysql.connection.commit()

    cur.close()

    return "ooooooppppppssss"

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/profile-user', methods=['POST'])
def user_profile():
    id = request.form['id']

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT avatar,email, name FROM user where id = %s",(id) )
    info = cur.fetchall()
    cur.close()
    
    info[0]['avatar'] = url_for('static', filename=info[0]['avatar'])

    return jsonify(info)


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/manager-product')
def manager_product():
    return render_template('manager-products.html')

@app.route('/edit-product')
def edit():


    return render_template('edit-product.html')


@app.route('/login/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/send_code', methods=['POST'])
def send_code():
    email = request.form['email']
    code = random_code(6)
    
    # session.pop('code', None)
    session['code'] = code
    import pdb; pdb.set_trace()


    gmail = []
    gmail.append(email)
    msg = Message( 
                'Code', 
                sender ='bbnam159@gmail.com', 
                recipients = gmail 
               ) 

    msg.body = 'Your code is ' + code 
    mail.send(msg) 
    

    return "OK"


@app.route('/check_code', methods=['POST'])
def check_code():
    code = request.form['code']
    if (session.get('code') == code):
        return jsonify(1)
    import pdb; pdb.set_trace()
    return jsonify(0)
 

@app.route('/login/forgot-password/check-code')
def check():
    return render_template('check_code.html')


@app.route('/search', methods=['POST'])
def search():

    search = request.form['search']

    query = '''
        SELECT *
        FROM shoes
        where name like '%{}%'
        '''.format(search)

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    shoes = cur.fetchall()
    cur.close()


    shoes = get_shoes_image_in_shoes(shoes)

    return jsonify(shoes)

@app.route('/admin-order')
def admin_order():
    return render_template('list-order.html')


@app.route('/done-order', methods=['POST'])
def done_order():
    id_order = request.form['id']
    query = '''
    UPDATE `order` SET state='done' WHERE id= {};
    '''.format(id_order)
    # import pdb; pdb.set_trace()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query)
    mysql.connection.commit()

    cur.close()

    return "Done"

@app.route('/upload-edit-product', methods=['POST'])
def upload_edit_product():
    asd = "image-"
    shoes_id = request.cookies.get('shoes')
    
    index_image = 0
    for i in range(6):
        string = asd + str(i + 1)
        index_image = i + 1
        file = request.files[string]
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                link = os.path.join(app.config['PRODUCT'], filename).replace('/home/nam/Desktop/Web/static/',"")
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                
                
                

                query_1 = '''
                select * from shoes_image where name = '{}'
                '''.format(link)
                cur.execute(query_1)
                has_image = cur.fetchall()
                

                query_2 = '''
                select id from shoes_image where index_image = {} and shoes_id = {}
                '''.format(index_image, shoes_id)
                cur.execute(query_2)
                image = cur.fetchone()

                # import pdb; pdb.set_trace()
                if (image is not None):
                    query_3 = '''
                    UPDATE `mydb`.`shoes_image` SET `index_image`=0 WHERE `shoes_id`={} and id = {};
                    '''.format(shoes_id, image['id'])
                    cur.execute(query_3)
                    mysql.connection.commit()

                if (has_image == ()):
                    query_4 = '''
                    INSERT INTO `mydb`.`shoes_image` (`name`, `shoes_id`, `index_image`) VALUES ('{}', {}, {});
                    '''.format(link, shoes_id, index_image)
                    cur.execute(query_4)
                    mysql.connection.commit()
                    
                else:
                
                    query = '''
                    UPDATE `mydb`.`shoes_image` SET `index_image`={} WHERE `shoes_id`={} and name = '{}';
                    '''.format(index_image, shoes_id, link)
                    
                    cur.execute(query)
                    mysql.connection.commit()

                cur.close()
                file.save(os.path.join(app.config['PRODUCT'], filename))

    return redirect(url_for('edit'))            

    
    


@app.route('/update-edit-product', methods=['POST'])
def update_edit_product():
    # import pdb; pdb.set_trace()
    name_size = request.form['name_size']
    length_size = request.form['length_size']
    product_name = request.form['product_name'].encode('utf-8')
    description = request.form['description'].encode('utf-8')
    categories = request.form['categories']
    price = request.form['price']
    id = request.form['id']


    # import pdb; pdb.set_trace()
    query = '''
    UPDATE `mydb`.`shoes` SET `name`="{}", `price`={}, 
    `categories_id`={}, 
    `description`="{}" WHERE `id`={};
    '''.format(product_name, price, categories, description, id)


    query_2 = '''
    UPDATE `mydb`.`specific_shoes` SET `amount`={} 
    WHERE `name`={} and`shoes_id`={};
    '''.format(length_size, name_size, id)



    query_3 = '''
    select * from specific_shoes where name = {} and shoes_id = {}
    '''.format(name_size, id)
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   
   
   
    cur.execute(query)
    mysql.connection.commit()

    cur.execute(query_3)
    
    
    if (cur.fetchall() == ()):
        query_4 = '''
        INSERT INTO `mydb`.`specific_shoes` 
        (`name`, `amount`, `shoes_id`) VALUES ('{}', {}, {});

        '''.format(name_size, length_size, id)
        cur.execute(query_4)
        mysql.connection.commit()
    else:
        cur.execute(query_2)
        mysql.connection.commit()
    


    

    cur.close()


    return "sadasd"

@app.route('/add-product')
def add_product():
    return render_template('add-product.html')


@app.route('/create-add-product', methods=['POST'])
def create_add_product():
    # import pdb; pdb.set_trace()
    name_size = request.form['name_size']
    length_size = request.form['length_size']
    product_name = request.form['product_name'].encode('utf-8')
    description = request.form['description'].encode('utf-8')
    categories = request.form['categories']
    price = request.form['price']
    


    # import pdb; pdb.set_trace()
    query = '''
    INSERT INTO `mydb`.`shoes` ( `name`, `price`, `categories_id`, `description`) 
    VALUES ('{}', {}, {}, '{}');

    '''.format(product_name, price, categories, description)

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   
   
    cur.execute(query)
    mysql.connection.commit()

    query_1 = '''
    select * from shoes
    '''

    cur.execute(query_1)
    shoes = cur.fetchall()

    query_4 = '''
        INSERT INTO `mydb`.`specific_shoes` 
        (`name`, `amount`, `shoes_id`) VALUES ('{}', {}, {});

        '''.format(name_size, length_size, len(shoes))

    cur.execute(query_4)
    mysql.connection.commit()

    
    # set_cookie('shoes', user)
    

    # query_4 = '''
    #     INSERT INTO `mydb`.`specific_shoes` 
    #     (`name`, `amount`, `shoes_id`) VALUES ('{}', {}, {});

    #     '''.format(name_size, length_size, id)
    # cur.execute(query_4)
    # mysql.connection.commit()

    

    cur.close()
    

    return "ASDSDA" 

@app.route('/create-image-product', methods=['POST'])
def create_image_product():
    asd = "image-"
    shoes_id = request.cookies.get('shoes')
    
    index_image = 0
    for i in range(6):
        string = asd + str(i + 1)
        index_image = i + 1
        file = request.files[string]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            link = os.path.join(app.config['PRODUCT'], filename).replace('/home/nam/Desktop/Web/static/',"")
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                
            query_4 = '''
                    INSERT INTO `mydb`.`shoes_image` (`name`, `shoes_id`, `index_image`) VALUES ('{}', {}, {});
                    '''.format(link, shoes_id, index_image)
            cur.execute(query_4)
            mysql.connection.commit()
            
           

               

            cur.close()
            file.save(os.path.join(app.config['PRODUCT'], filename))
                    

    return redirect(url_for('manager_product'))            

if __name__ == "__main__":
	app.run(debug= True)

