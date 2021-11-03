from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy

import sys


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)

class History2(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=True, default="System")
    message = db.Column('message', db.String)

#쿼리 전체 삭제
#History2.query.delete()
#db.session.commit()

@app.route('/')
def index():
    messages = History2.query.all()
    return render_template('index.html', messages=messages)

@socketio.on('my event')
def handle_my_custom_event(msg, methods=['GET', 'POST']):
    #name = list(msg.keys())
    #message = list(msg.values())
    #message = History2(message=message[0], name=name[0])
    name = msg.get('name')
    message = msg.get('message')
    insertMessage = History2(name=name, message=message)
    db.session.add(insertMessage)
    db.session.commit()
    
    print(msg, file=sys.stdout)

    socketio.emit('my response', msg)






if __name__ == '__main__':
    socketio.run(app, debug=True)