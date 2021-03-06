from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy

import sys
faberId = "id"

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
#deletex = db.session.query(History2).delete()

@app.route('/')
def index():
    messages = History2.query.all()
    return render_template('index.html', messages=messages)

@app.route('/credential')
def credential():
    return render_template('credential.html')

@app.route("/invitation")
def invitation() :
    if "invitation" in session :
        print("invitation: " + faberId, file=sys.stdout)
        return render_template("invitation.html", invitation=True)
    else :
        return render_template("invitation.html", invitation=False)

@app.route("/processCreateInvitation", methods=["POST"])
def processCreateInvitation() :
    session["invitation"] = True
    faberId = request.form.get("faberId")
    global aliceId
    aliceId = request.form.get("aliceId")

    return redirect(url_for("invitation"))

@app.route("/processDeleteInvitation", methods=["POST"])
def processDeleteInvitation():
    session.pop("invitation", None)
    return redirect(url_for("invitation"))






@socketio.on('my event')
def handle_my_custom_event(msg, methods=['GET', 'POST']):
    name = msg.get('name')
    message = msg.get('message')
    insertMessage = History2(name=name, message=message)
    db.session.add(insertMessage)
    db.session.commit()
    socketio.emit('my response', msg)

@socketio.on('connect_inter')
def handle_my_custom_event2(msg, methods=['GET', 'POST']):
    socketio.emit('my response', msg)




if __name__ == '__main__':
    socketio.run(app, debug=True)
