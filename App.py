from flask import Flask, render_template, request, redirect, url_for, session

#not needed since Flask uses a similar method to escape user input to prevent injection type attacks
#from markupsafe import escape
import mysql.connector
from argon2 import PasswordHasher


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret
ph = PasswordHasher()

# Connect to the database
#global value so it can easily be changed in the future if needed
#and 
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Welcome123!!",
    database = "websitedatabase"
)
mycursor = mydb.cursor()


@app.route('/')
def index():
    return render_template('LoginScreen.html')

@app.route('/loggingIn', methods=['POST'])
def loggingIn():
    username = request.form['username']
    password = request.form['password']

    #this checks to see if we have any inputs that are empty so we don't add them to the database
    if username is None or password is None:
        return render_template('LoginScreen.html', error="Please enter both username and password")

    query = "SELECT password FROM Users WHERE username = %s"
    mycursor.execute(query, (username,))
    result = mycursor.fetchone()
    if result:
        stored_password = result[0]
        if ph.verify(stored_password, password):
            return render_template('HomeScreen.html', username=username)
    return render_template('LoginScreen.html', error="Invalid username or password")



@app.route('/registerScreen', methods=['GET'])
def registerScreen():
    return render_template('RegisterScreen.html')

@app.route('/registerAction', methods=['POST'])
def registerAction():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    hashedPassword = ph.hash(password)

    #this checks to see if we have any inputs that are empty so we don't add them to the database
    if username is None or password is None or email is None:
        return render_template('RegisterScreen.html', error="Please fill in all fields")

    # check if user is added to the database since the username is unique
    query = "SELECT CASE WHEN EXISTS (SELECT 1 FROM Users WHERE username = %s) THEN 1 ELSE 0 END FOR UPDATE"
    mycursor.execute(query, (username,))
    mydb.commit()  # Commit the transaction to release the lock
    result = mycursor.fetchone()[0]
    if result == 0:
        # User does not exist, so we can add them
        query = "INSERT INTO Users (username, password, email) VALUES (%s, %s, %s) FOR UPDATE"
        mycursor.execute(query, (username, hashedPassword, email))
        mydb.commit()
        return render_template('LoginScreen.html', message="Registration successful. Please login.")
    else:
        return render_template('RegisterScreen.html', error="Username already exists")

if __name__ == '__main__':
    app.run(debug=True)