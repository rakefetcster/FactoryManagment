from flask import Blueprint,jsonify, request, make_response
from BLL.auth_bl import AuthBL

auth = Blueprint('auth', __name__)
auth_bl = AuthBL()

@auth.route("/login", methods=['POST'])
def login():
    username = request.json["username"]
    email = request.json["email"]
    token = auth_bl.get_token(username,email)
    if token != None:
        return make_response({"token":token,"count_enties":0},200)
    else:
        return make_response({"error":"you aren't authorized"},401)

