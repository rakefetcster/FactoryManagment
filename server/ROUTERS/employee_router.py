from flask import Blueprint,jsonify, request, make_response
from BLL.employee_bl import Employee
from BLL.user_bl import UserBL
users_bl = UserBL()

emp = Blueprint('employee', __name__)
employee_bl = Employee()

def condition_jwt():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist,user_fullName,autorized = users_bl.check_user(token)
        return exist,user_fullName,autorized
    else:
        return False,'',True

@emp.route("/", methods=['GET'])
def get_employees():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        empObj = employee_bl.get_all_employee(user_fullName)
        for emp in empObj:
            if "Error" in emp:
                return make_response(emp,400)
        return make_response(jsonify(empObj),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)
    

@emp.route("/<id>", methods=['GET'])
def get_employees_by_id(id):
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        empObj = employee_bl.get_employee_by_id(id)
        for emp in empObj:
            if "Error" in emp:
                return make_response(emp,400)
        return make_response(jsonify(empObj),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)
    

@emp.route("/", methods=['POST'])
def insert_employee():
    exist, user_fullName, autorized = condition_jwt()
    if exist==True:
        obj=request.json
        result = employee_bl.add_new_employee(obj)
        for res in result:
            if "Error" in res:
                return make_response(res,400)
        return make_response(jsonify(result),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)

@emp.route("/<id>",methods=['PUT'])
def update_emploee(id):
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        obj = request.json
        result = employee_bl.update_employee(id,obj)
        for res in result:
            if "Error" in res:
                return make_response(res,400)
        return make_response(jsonify(result),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)


@emp.route("/<id>",methods=['DELETE'])
def delete_emp(id):
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        result = employee_bl.delete_employee(id)
        for res in result:
            if "Error" in res:
                return make_response(res,400)
        return make_response(jsonify(result),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)