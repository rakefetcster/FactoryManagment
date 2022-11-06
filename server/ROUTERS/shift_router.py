from flask import Blueprint,jsonify, request, make_response
from BLL.shift_bl import ShiftBL
shi = Blueprint('shift', __name__)
shifts_bl = ShiftBL()
from BLL.user_bl import UserBL
users_bl = UserBL()


def condition_jwt():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist,user_fullName,autorized = users_bl.check_user(token)
        return exist,user_fullName,autorized
    else:
        return False,'',True

        
#Get All
@shi.route("/", methods=['GET'])
def get_all_shifts():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        the_shifts = shifts_bl.get_shifts(user_fullName)
        for shift in the_shifts:
            if "Error" in shift:
                return the_shifts
        return make_response(jsonify(the_shifts),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)
    

@shi.route("/<id>", methods=['GET'])
def get_shift(id):
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        shiftObj = shifts_bl.get_one_shift(id)
        for shift in shiftObj:
            if "Error" in shift:
                return shiftObj
        return make_response(jsonify(shiftObj),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)
    

@shi.route("/<id>", methods=['PUT'])
def update_shift(id):
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        obj = request.json
        result = shifts_bl.update_this_shift(id,obj)
        for shift in result:
            if "Error" in shift:
                return result
        return make_response(jsonify(result),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)
    

@shi.route("/", methods=['POST'])
def new_shift():
    exist,user_fullName,autorized = condition_jwt()
    if exist==True:
        obj = request.json
        result = shifts_bl.create_new_shift(obj)
        for shift in result:
            if "Error" in shift:
                return result
        return make_response(jsonify(result),200)
    elif autorized == False: 
        return make_response({"Error_autorized":"You have reach the max number of Actions for today"},401)
    else:
        return make_response({"Error":"Not authorized"},401)
    