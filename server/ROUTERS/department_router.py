from flask import Blueprint,jsonify, request, make_response
from BLL.department_bl import DepartmentBl
from BLL.user_bl import UserBL
users_bl = UserBL()

dep = Blueprint('department', __name__)
department_bl = DepartmentBl()


def condition_jwt():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist,user_fullName,autorized = users_bl.check_user(token)
        return exist,user_fullName,autorized
    else:
        return False,'',True

#Get All
@dep.route("/", methods=['GET'])
def get_all_departments():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        depObj = department_bl.get_departments(user_fullName)
        for dep in depObj:
            if "Error" in dep:
                return make_response(dep,400)
        return make_response(jsonify(depObj),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)

@dep.route("/<id>", methods=['GET'])
def get_department_by_id(id):
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        depObj = department_bl.get_department_id(id)
        for dep in depObj:
            if "Error" in dep:
                return make_response(dep,400)
        return make_response(jsonify(depObj),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)

@dep.route("/<id>", methods=['PUT'])
def update_department(id):
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        obj = request.json
        result = department_bl.update_department_by_id(id,obj)
        for dep in result:
            if "Error" in dep:
                return make_response(dep,400)
        return make_response(jsonify(result),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)


@dep.route("/", methods=['DELETE'])
def delete_department():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        obj = request.json
        result = department_bl.deletet_department_by_id(obj)
        for dep in result:
            if "Error" in dep:
                return make_response(dep,400)
        return make_response(jsonify(result),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)


@dep.route("/", methods=['POST'])
def add_department():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        obj = request.json
        depObj = department_bl.add_new_department(obj)
        for dep in depObj:
            if "Error" in dep:
                return make_response(dep,400)
        return make_response(jsonify(depObj),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)
