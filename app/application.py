import json

from uuid import uuid4
from flask import Flask, request, redirect, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from dynamodb_util import DynamoDBUtil
from constants import *

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = str(uuid4())

jwt = JWTManager(app)

cache_table = DynamoDBUtil(table_name=GPT_APP_CACHE_TABLE_NAME, pk_name=CACHE_KEY_NAME)


@app.route("/")
def home():
    return "OAuth 2.0 server demo"


@app.get("/authorize")
def authorize():
    """
    authorization page

    :return:
    """

    client_id = request.args.get("client_id")
    state = request.args.get("state")

    # if client_id not in TEST_CLIENTS:
    #     return "Invalid client_id", 400

    redirect_uri = request.args.get("redirect_uri") + "?state=" + state

    return f'''
        <form method="post", action="/login">
            <input type="hidden" name="client_id", value="{client_id}"/>
            <input type="hidden" name="redirect_uri", value="{redirect_uri}"/>
            <input type="hidden" name="state", value="{state}"/>
            <input type="text" name="username" placeholder="Username" />
            <input type="password" name="password" placeholder="Password" />
            <input type="submit" value="Login" />
        </form>
    '''


@app.post("/login")
def login():
    """
    login user & redirect to gpt redirect_url

    :return:
    """
    username = request.form.get("username")
    password = request.form.get("password")
    if TEST_USERS[username]["password"] != password:
        return "Unauthorized", 401

    client_id = request.form.get("client_id")
    redirect_uri = request.form.get("redirect_uri")
    state = request.form.get("state")

    code = str(uuid4())

    cache_table.save(item={
        "cache_key": code,
        "username": username,
        "client_id": client_id,
        "state": state
    })

    return redirect(redirect_uri + "&code=" + code)


@app.post("/token")
def get_token():
    """
    exchange tokens with codes

    :return:
    """
    client_id = request.form.get("client_id")
    client_secret = request.form.get("client_secret")
    code = request.form.get("code")

    cached_record = cache_table.get(code)

    if not cached_record:
        return "Invalid code", 400
    # if client_secret != TEST_CLIENTS[client_id]:
    #     return "Unauthorized", 401

    return jsonify(
        access_token=create_access_token(identity=cached_record["username"]),
        token_type="bearer"
    )


@app.get("/users/me")
@jwt_required()
def get_user_info():
    uid = get_jwt_identity()
    return {
        "full_name": TEST_USERS[uid]["full_name"]
    }


if __name__ == "__main__":
    app.run(debug=True)
