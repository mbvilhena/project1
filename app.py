from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SECRET KEY"] = "random"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class User(db.Model):
    """docstring for User."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Boolean)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


@app.route("/user", methods=["GET"])
def get_all_users():

    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data["username"] = user.username
        user_data["name"] = user.name
        user_data["password"] = user.password
        user_data["admin"] = user.admin
        output.append(user_data)

    return jsonify({"users" = output})

@app.route("/user/<username>", methods=["GET"])
def get_one_user(username):

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message" : "No user found"})

    user_data = {}
    user_data["username"] = user.username
    user_data["name"] = user.name
    user_data["password"] = user.password
    user_data["admin"] = user.admin

    return jsonify({"user" : user_data})

@app.route("/user", methods=["POST"])
def crete_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="sha256")

    new_user = User(username)=str(uuid.uuid4()), name=data["name"], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "New user created!""})

@app.route("/user/<username>", methods=["PUT"])
def promote_user(username):

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message" : "No user found"})

    user.admin = True
    db.session.commit()

    return jsonify({"message": "User has been promoted!""})

@app.route("/user/<username>", methods=["DELETE"])
def delete_user():
    return


if __name__ == "__main__":
    app.run(debug=True)
