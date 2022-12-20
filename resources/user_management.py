from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db, UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from dbconnection.redis_connect import blocklist_connection
from datetime import timedelta

blp = Blueprint("Users", __name__, description="User Management")


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel()
        user.user_name = user_data["user_name"]
        user.password = generate_password_hash(
            user_data["password"], method="pbkdf2:sha256")

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as err:
            abort(404, message=str(err))
        else:
            return user

    @blp.arguments(UserSchema)
    @jwt_required()
    def put(self, user_data):
        user = UserModel.query.filter(
            UserModel.user_name == user_data["user_name"]).first()
        if not user:
            abort(404, message="User does not exist")
        return {"msg": "Password Change success"}, 200


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def get(self, user_data):
        user = UserModel.query.filter(
            UserModel.user_name == user_data["user_name"]).first()
        if not user:
            abort(404, message="User not found")
        if not (check_password_hash(user.password, user_data["password"])):
            abort(404, message="Incorrect Password")
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}


@blp.route("/logout/<int:user_id>")
class Logout(MethodView):
    @jwt_required()
    def post(self, user_id):
        if not user_id == get_jwt_identity():
            abort(404, "User not logged in")

        jti = get_jwt()["jti"]
        blocklist_connection.set(jti, "", ex=timedelta(hours=0.5))
        return {"msg": "Access token revoked"}
