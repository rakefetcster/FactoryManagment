from flask import Blueprint,jsonify, request, make_response
from BLL.user_bl import UserBL
users = Blueprint('users', __name__)
users_bl = UserBL()


def condition_jwt():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist,user_fullName,autorized = users_bl.check_user(token)
        return exist,user_fullName,autorized
    else:
        return False,'',True

#Get All
@users.route("/", methods=['GET'])
def get_all_users():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        users = users_bl.get_users(user_fullName)
        return make_response(jsonify(users),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)


@users.route("/get_user", methods=['GET'])
def get_user_name():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        userObj = {"user_name":user_fullName}
        return make_response(jsonify(userObj),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)
    