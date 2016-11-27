from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL
from werkzeug.security import generate_password_hash,check_password_hash
app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Password'
app.config['MYSQL_DATABASE_DB'] = 'wordliners'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    conn = mysql.connect()
    cursor = conn.cursor()
    _hashed_password = generate_password_hash(_password)

    cursor.callproc('createUser',(_name, _email, _hashed_password))
    # validate the received values
    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})

if __name__ == '__main__':
    app.run()