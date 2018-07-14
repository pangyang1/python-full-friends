from flask import Flask, render_template, request, redirect, session
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'Secret'
mysql = MySQLConnector(app, 'mydb')

@app.route('/')
def home():

    friends = mysql.query_db("SELECT name, age, DATE_FORMAT(created_at, '%M %d, %Y') AS friends_from FROM friends")

    data = {}
    data['name'] = "<div>"
    data['age'] = "<div>"
    data['friend_since'] = "<div>"

    for i in range(0, len(friends)):
        data['name'] += '<p class="cell">' + str(friends[i]['name']) +'</p>'
        data['age'] += '<p class="cell">' + str(friends[i]['age']) + '</p>'
        data['friend_since'] += '<p class="cell">' + str(friends[i]['friends_from']) + '</p>'

    data['name'] += "</div>"
    data['age'] += "</div>"
    data['friend_since'] += "</div>"
    return render_template('index.html', data = data)

@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friends(name,age,created_at,updated_at) VALUES (:name,:age,now(),now())"
    print request.form['name']
    print request.form['age']

    new_data ={
        'name': request.form['name'],
        'age': request.form['age']
    }

    mysql.query_db(query, new_data)
    return redirect('/')

app.run(debug=True)
