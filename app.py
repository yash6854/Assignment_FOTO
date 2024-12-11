from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from database import db, bcrypt, User, Book, BorrowRequest
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

@app.route('/init', methods=['GET'])
def init_db():
    try:
        db.create_all()
        if not User.query.filter_by(email='admin@example.com').first():
            admin_user = User(
                email='admin@example.com',
                password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                role='admin'
            )
            db.session.add(admin_user)

        if not Book.query.all():
            books = [
                Book(title='Book 1', author='Author 1', isbn='1234567890', availability=True),
                Book(title='Book 2', author='Author 2', isbn='0987654321', availability=True)
            ]
            db.session.bulk_save_objects(books)

        db.session.commit()
        return jsonify({"message": "Database initialized and seeded"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity={"email": user.email, "role": user.role}, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": access_token}), 200

@app.route('/admin/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_password, role='user')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user": {"email": new_user.email, "role": new_user.role}}), 201

@app.route('/books', methods=['GET'])
@jwt_required()
def list_books():
    books = Book.query.all()
    return jsonify([{
        "id": b.id,
        "title": b.title,
        "author": b.author,
        "isbn": b.isbn,
        "availability": b.availability
    } for b in books]), 200

if __name__ == '__main__':
    app.run(debug=True)
