from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash,check_password_hash
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:db1234@localhost:5432/hotel_api"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

    def __init__(self, public_id, name, password, admin):
        self.public_id =public_id
        self.name = name
        self.password = password
        self.admin = admin

class HotelsModel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    location = db.Column(db.String())
    doRecommend = db.Column(db.Boolean)
    rating = db.Column(db.Integer())
    feedback =db.Column(db.Text())

    def __init__(self, name, location, doRecommend, rating, feedback):
        self.name = name
        self.location = location
        self.doRecommend = doRecommend
        self.rating = rating
        self.feedback = feedback


    def __repr__(self):
        return f"<Hotel {self.name}>"

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    passwd = generate_password_hash(data['password'], method='sha256')
    new_user = UserModel(public_id=str(uuid.uuid4()), name=data['name'],password=passwd, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created successfully'})

@app.route('/user/hotels', methods=['POST', 'GET'])
def handle_hotels():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_hotel = HotelsModel(name=data['name'], location=data['location'], doRecommend=data['doRecommend'], rating=data['rating'], feedback=data['feedback'])
            db.session.add(new_hotel)
            db.session.commit()
            return jsonify({"message": f"hotel {new_hotel.name} has been created successfully."})
        else:
            return jsonify({"error": "The request payload is not in JSON format"})

    elif request.method == 'GET':
        hotels = HotelsModel.query.all()
        results = [
            {
                "name": hotel.name,
                "location": hotel.location,
                "doRecommend": hotel.doRecommend,
                "rating":hotel.rating,
                "feedback": hotel.feedback

            } for hotel in hotels]



if __name__ == '__main__':
    app.run(debug=True)