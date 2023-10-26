from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import login_required
from flask_mysqldb import MySQL
from models import Model
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import mysql.connector
import re
import os
from flask import jsonify
from models import Model
from flask import Response
from flask import request
import json

model = Model()

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '541793'

app.config['SECRET_KEY'] = '@#$123456&*()'
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + \
   '/static/images'
app.config['MAX_CONTENT_PATH'] = 10000000

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mywebsite'

# Intialize MySQL
mysql = MySQL(app)

global getJenis

@app.route('/')
def index():    
   return render_template('index.html')

@app.route('/mlebet_rien', methods=["GET","POST"])
def login():
    msg = ''    
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        # model = passing()
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id_user'] = account['id_user']
            session['username'] = account['username']
            # Redirect to home page            
            # model.setLogin(status)            
            return redirect("http://localhost:5000/dashboard")
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/logout', methods=["GET","POST"])
def logout():
    session.pop('id_user')    
    return render_template('index.html')

@app.route('/dashboard', methods=["GET","POST"])
def dashboard():
  if session.get('id_user'):   
    return render_template('dashboard.html')
  else :
    return render_template('index.html')
  
@app.route('/furniture', methods=["GET","POST"])
def furniture():  
  if session.get('id_user'):

    if request.method == 'POST':
      if request.form['btnHapus'] == "hapus":
        app.logger.info(model.getidJenis())        
      else : 
        app.logger.info('NO')


    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT p.gambar, p.nama_produk, b.nama_bahan, p.harga, p.status, p.id_produk, p.deskripsi FROM produk p JOIN bahan b ON p.id_bahan=b.id_bahan
                      JOIN jenis_produk j ON p.id_jenis_produk=j.id_jenis_produk AND nama_jenis_produk = "furniture" ''')
    rv = cursor.fetchall()
    images = os.listdir(os.path.join(app.static_folder, "images"))

    return render_template('furniture.html', value=rv)
  else :
    return render_template('index.html')

#JSON
@app.route('/furniture/getJSON', methods=["GET","POST"])
def furnitureJSON():  
  if session.get('id_user'):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT p.gambar, p.nama_produk, b.nama_bahan, p.harga, p.status, p.id_produk, p.deskripsi FROM produk p JOIN bahan b ON p.id_bahan=b.id_bahan
                      JOIN jenis_produk j ON p.id_jenis_produk=j.id_jenis_produk AND nama_jenis_produk = "furniture" ''')    

    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()    
    json_data=[]

    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    return json.dumps({'data':json_data})
  else :
    return render_template('index.html')


@app.route('/editFurniture/<id_produk>', methods=["GET","POST"])
def editFurniture(id_produk):  
  if session.get('id_user'):
    if request.method == 'POST':
      nama_produk = request.form['txtNamaProduk']
      harga = request.form['txtHarga']
      deskripsi = request.form['txtDeskripsi']
      status = request.form['rbJenis']

      app.logger.info(nama_produk)
      app.logger.info(harga)
      app.logger.info(deskripsi)
      app.logger.info(status)

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE produk set nama_produk=%s, harga=%s, deskripsi=%s, status=%s WHERE id_produk=%s", 
                  (nama_produk,harga,deskripsi,status,id_produk,))
    mysql.connection.commit()

    return redirect(url_for('furniture'))
  else :
    return render_template('index.html')


@app.route('/hapusFurniture/<id_produk>', methods=["POST"])
def hapusFurniture(id_produk):  
  if session.get('id_user'):

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM produk WHERE id_produk=%s", (id_produk,))
    mysql.connection.commit()
    
    return redirect(url_for('furniture'))
  else :
    return render_template('index.html')
     

@app.route('/tata_busana', methods=["GET","POST"])
def tata_busana():
  if session.get('id_user'):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT p.gambar, p.nama_produk, b.nama_bahan, p.harga, p.status, p.id_produk, p.deskripsi FROM produk p JOIN bahan b ON p.id_bahan=b.id_bahan
                      JOIN jenis_produk j ON p.id_jenis_produk=j.id_jenis_produk AND nama_jenis_produk = "busana" ''')
    rv = cursor.fetchall()    
    images = os.listdir(os.path.join(app.static_folder, "images"))     
    return render_template('tata_busana.html', value=rv)    
  else : 
    return render_template('index.html')

@app.route('/editBusana/<id_produk>', methods=["GET","POST"])
def editBusana(id_produk):  
  if session.get('id_user'):
    if request.method == 'POST':
      nama_produk = request.form['txtNamaProduk']
      harga = request.form['txtHarga']
      deskripsi = request.form['txtDeskripsi']
      status = request.form['rbJenis']

      app.logger.info(nama_produk)
      app.logger.info(harga)
      app.logger.info(deskripsi)
      app.logger.info(status)

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE produk set nama_produk=%s, harga=%s, deskripsi=%s, status=%s WHERE id_produk=%s", 
                  (nama_produk,harga,deskripsi,status,id_produk,))
    mysql.connection.commit()

    return redirect(url_for('tata_busana'))
  else :
    return render_template('index.html')


@app.route('/hapusBusana/<id_produk>', methods=["POST"])
def hapusBusana(id_produk):  
  if session.get('id_user'):

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM produk WHERE id_produk=%s", (id_produk,))
    mysql.connection.commit()
    
    return redirect(url_for('tata_busana'))
  else :
    return render_template('index.html')


@app.route('/detailProduk/<id_produk>', methods=["GET","POST"])
def detailProduk(id_produk):  
  if session.get('id_user'):

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT p.gambar, p.nama_produk, b.nama_bahan, p.harga, p.status, p.id_produk, p.deskripsi FROM produk p JOIN bahan b ON p.id_bahan=b.id_bahan
                      JOIN jenis_produk j ON p.id_jenis_produk=j.id_jenis_produk AND id_produk = %s ''' , (id_produk,))
    detail = cursor.fetchall()
    images = os.listdir(os.path.join(app.static_folder, "images"))
    return render_template('detailProduk.html', value=detail)
  else :
    return render_template('index.html')

@app.route('/tambah_produk', methods=["GET","POST"])
def tambah_produk():  
  if session.get('id_user'):       
    if request.method == 'POST':

      nmProduk = request.form['txtNamaProduk']
      harga = request.form['txtHarga']
      deskripsi = request.form['txtDeskripsi']
      status = request.form['rbJenis']

      #load Jenis Produk
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM jenis_produk')        
      getJenis = cursor.fetchall()
      select = request.form.get('jnsProduk')
      app.logger.info(select)
      #get id Jenis produk              
      cursor.execute('SELECT id_jenis_produk FROM jenis_produk WHERE nama_jenis_produk = %s ', [select])      
      tmp = cursor.fetchall()
      ans_con=(str(tmp))
      idJns = re.sub(r'\W', '', ans_con)      

      #load bahan
      cursor.execute('SELECT nama_bahan FROM bahan')
      getBahan = cursor.fetchall()
      bahan = request.form.get('bahan')
      #get id bahan              
      cursor.execute('SELECT id_bahan FROM bahan WHERE nama_bahan = %s ', [bahan])
      tmp2 = cursor.fetchall()
      ans_con=(str(tmp2))
      idBahan = re.sub(r'\W', '', ans_con)      

      f = request.files['file']
      filename = app.config['UPLOAD_FOLDER'] + \
         '/' + secure_filename(f.filename)     

      cursor.execute('''INSERT INTO produk(gambar, nama_produk, id_jenis_produk, id_bahan, harga, deskripsi, status) 
           VALUES(%s,%s,%s,%s,%s,%s,%s)''', (f.filename, nmProduk, idJns, idBahan, harga, deskripsi, status))
      mysql.connection.commit()

      try:
         f.save(filename)                  
      except:
         print(filename)
         return render_template('upload_gagal.html', 
            filename=secure_filename(f.filename))     

   #load Jenis Produk
    cursor = mysql.connection.cursor()
   # cursor2 = mysql.connection.cursor()
    cursor.execute('SELECT * FROM jenis_produk')    
   # cursor.execute('SELECT id_jenis_produk FROM jenis_produk WHERE nama_jenis_produk = %s', )
    getJenis = cursor.fetchall()

    cursor.execute('SELECT nama_bahan FROM bahan')
    getBahan = cursor.fetchall()
   
    return render_template('tambah_produk.html', value=getJenis, value2=getBahan)
  else:
    return render_template('index.html')    
     

# ------------------ for guest ------------------------
@app.route('/furniture_guest', methods=["GET","POST"])
def furniture_guest():  
  cursor = mysql.connection.cursor()
  cursor.execute('''SELECT p.gambar, p.nama_produk, b.nama_bahan, p.harga, p.status, p.id_produk, p.deskripsi FROM produk p JOIN bahan b ON p.id_bahan=b.id_bahan
                    JOIN jenis_produk j ON p.id_jenis_produk=j.id_jenis_produk AND nama_jenis_produk = "furniture" ''')
  rv = cursor.fetchall()
  images = os.listdir(os.path.join(app.static_folder, "images"))

  return render_template('furniture_guest.html', value=rv)


@app.route('/tata_busana_guest', methods=["GET","POST"])
def tata_busana_guest():  
  cursor = mysql.connection.cursor()
  cursor.execute('''SELECT p.gambar, p.nama_produk, b.nama_bahan, p.harga, p.status, p.id_produk, p.deskripsi FROM produk p JOIN bahan b ON p.id_bahan=b.id_bahan
                    JOIN jenis_produk j ON p.id_jenis_produk=j.id_jenis_produk AND nama_jenis_produk = "busana" ''')
  rv = cursor.fetchall()    
  images = os.listdir(os.path.join(app.static_folder, "images"))     
  return render_template('tata_busana_guest.html', value=rv)    
  

if __name__ == '__main__':
   app.run(debug=True)
