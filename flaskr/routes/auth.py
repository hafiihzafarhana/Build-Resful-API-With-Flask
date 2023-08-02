from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
import validators
from flaskr.database.database import User, db
from flask_jwt_extended import create_access_token, create_refresh_token

# auth menajadi nama
# __name__ digunakan untuk mengatur dimana blueprint akan berjalan
auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.post("/register")
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({
            'message': "Your password is short. Minimum length password is 6"
        }), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({
            'message': "Your username is short. Minimum length username is 6"
        }), HTTP_400_BAD_REQUEST

    # should 0-9 and a-z
    if not username.isalnum() or " " in username:
        return jsonify({
            'message': "Your username is should alpha numeric and no spacing"
        }), HTTP_400_BAD_REQUEST

    # is email or not?
    if not validators.email(email):
        return jsonify({
            'message': "This is not satisfied email"
        }), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            'message': "Email is taken"
        }), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            'message': "Username is taken"
        }), HTTP_409_CONFLICT

    password_hash = generate_password_hash(password)

    user = User(username=username, password=password_hash, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User registered',
        'status': 'CREATED',
        'data': {
            "username": username,
            "email": email,
            "password": password_hash,
        }
    }), HTTP_201_CREATED


@auth.get("/me")
def me():
    return "me"


@auth.post("/login")
def login():
    #  ' ' is default value
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:
        is_past_correct = check_password_hash(user.password, password)

        if is_past_correct:
            refresh_token = create_refresh_token(identity=user.id)
            access_token = create_access_token(identity=user.id)

            return jsonify({
                'message': 'User login',
                'status': 'OK',
                'data': {
                    "refresh_token": refresh_token,
                    "access_token": access_token,
                }
            }), HTTP_200_OK

    return jsonify({
        'message': "User not found"
    }), HTTP_404_NOT_FOUND
