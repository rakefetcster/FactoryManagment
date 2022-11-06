from flask import Blueprint,jsonify, request, make_response
from BLL.shift_emp_bl import ShiftEmp
from BLL.user_bl import UserBL
users_bl = UserBL()

shi_emp = Blueprint('shift_emp', __name__)
shift_emp_bl = ShiftEmp()

def condition_jwt():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist,user_fullName,autorized = users_bl.check_user(token)
        return exist,user_fullName,autorized
    else:
        return False,'',True

@shi_emp.route("/", methods=['GET'])
def get_shift_emp():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        empObj = shift_emp_bl.get_all_shift_emp()
        for emp in empObj:
            if "Error" in emp:
                return empObj
        return make_response(jsonify(empObj),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)

@shi_emp.route("/",methods=['POST'])
def create_shiftEmp():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        obj = request.json
        result = shift_emp_bl.create_new_shiftEmp(obj)
        for res in result:
            if "Error" in res:
                return result
        return make_response(jsonify(result),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)


