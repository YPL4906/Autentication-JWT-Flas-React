from flask import Blueprint, request, jsonify
from .models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import cross_origin

api = Blueprint("api", __name__)

@api.route("/signup", methods=["POST", "OPTIONS"])
@cross_origin(origin="https://reimagined-cod-wqpjg6jxqxv3946g-3000.app.github.dev")
def signup():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@api.route("/token", methods=["POST", "OPTIONS"])
@cross_origin(origin="https://reimagined-cod-wqpjg6jxqxv3946g-3000.app.github.dev")
def login():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "email": user.email}), 200


@api.route("/private", methods=["GET", "OPTIONS"])
@cross_origin(origin="https://reimagined-cod-wqpjg6jxqxv3946g-3000.app.github.dev")
@jwt_required()
def private():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    user_id = get_jwt_identity()
    return jsonify({"msg": f"Welcome user {user_id}!"}), 200

