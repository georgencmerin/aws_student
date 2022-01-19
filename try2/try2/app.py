from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
 
app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"

mysql = MySQL()
import aws_credentials as rds  
# MySQL configurations
conn = pymysql.connect(
        host= rds.host, #endpoint link
        port = rds.port, # 3306
        user = rds.user, # admin
        password = rds.password, #adminadmin
        db = rds.db, #test

#import aws_credentials as rds   
#mysql = MySQL()
   
# MySQL configurations                                  
# app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
#app.config['MYSQL_DATABASE_DB'] = 'testingdb'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)
 
)
@app.route('/')
def Index():
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM employee')
    data = cur.fetchall()
  
    cur.close()
    return render_template('index.html', employee = data)
 
@app.route('/add_employee', methods = ['POST', 'GET'])
def add_employee():
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        name = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur.execute("INSERT INTO employee (fullname, email, phone) VALUES (%s,%s,%s)", (name, email, phone))
        conn.commit()
        flash('Student Added successfully')
        return redirect(url_for('Index'))
 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  

    cur.execute('SELECT * FROM employee WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', employee = data[0])
 
@app.route('/update/<id>', methods = ['POST', 'GET'])
def update_employee(id):
    if request.method == 'POST':
        name = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE employee
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (name, email, phone, id))
        flash('Student Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    #conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM employee WHERE id = {0}'.format(id))
    conn.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('Index'))
 
# starting the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)