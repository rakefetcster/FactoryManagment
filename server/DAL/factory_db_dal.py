
from pymongo import MongoClient
from bson import ObjectId

class FactoryDBDal:
    def __init__(self):
        self.__client = MongoClient(port=27017)
        self.__db = self.__client["factory"]
        self.__collection_emp = self.__db["employees"]
        self.__collection_dep = self.__db["departments"]
        self.__collection_shift = self.__db["shifts"]
        self.__collection_shiftemp = self.__db["shift_emp"]
        self.__collection_users = self.__db["users"]

    def get_all_employee(self):
        result_list = list()
        try:
            result_list = list(self.__collection_emp.find({}))
            return result_list
        except Exception as e:
            return [{"Error":"An error occurred"}]

    def insert_new_employee(self,empObj):
        try:
            self.__collection_emp.insert_one(empObj)
            return [{"Success":"created with id: {}".format(str(empObj["_id"]))}]
        except Exception as e:
            return [{"Error":"An error occurred"}]
            
    def get_one_employee(self,id):
        try:
            employee = self.__collection_emp.find_one({"_id":ObjectId(id)})
            return employee
        except Exception as e:
            return {"Error":"An error occurred"}

    def update_employee(self,id,empObj):
        try:
            if "departmentId" in empObj:
                empObj.update({"departmentId":ObjectId(empObj["departmentId"])})
                self.__collection_emp.update_one({"_id": ObjectId(id)},{"$set":empObj})
                return [{"Success":"The employee has been updated"}]
            else:
                return [{"Error":"An error occurred - The employee has not been updated"}]
        except Exception as e:
            return [{"Error":"An error occurred - The employee has not been updated" }]

    def insert_shift_to_emp(self,id,shiftObj):
        try:
            self.__collection_emp.update_one({"_id": ObjectId(id)},{"$set":{"shifts":[ObjectId(shiftObj)]}})
            return {"Success": "employee updated with shift"}
        except Exception as e:
            return {"Error":"An error occurred"}
    
    def insert_all_shift(self,id,shiftObj):
        try:
            self.__collection_emp.update_one({"_id": ObjectId(id)},{"$set":{"shifts":ObjectId(shiftObj)}})
            return {"Success": "The shift was entered"}
        except Exception as e:
            return {"Error":"An error occurred"}

    def delete_one_field_from_emp(self,obj):
        try:
            self.__collection_emp.update_many({ },{'$unset':obj})
            return {"Success": "deleted "}
        except Exception as e:
            return {"Error":"An error occurred"}

    def delete_this_employee(self,id):
        try:
            self.__collection_emp.delete_one({"_id": ObjectId(id)})
            return [{"Success":"employee deleted" }]
        except Exception as e:
            return [{"Error":"An error occurred - the employee was not deleted" }]

    def get_employees_by_department_id(self,id):
        try:
            employess = self.__collection_emp.find({"departmentId":ObjectId(id)})
            return employess
        except Exception as e:
            return [{"Error":"An error occurred"}]


#**********Department*************
    def get_all_departments(self):
        result_list = list()
        try:
            result_list = list(self.__collection_dep.find({}))
            return result_list
        except Exception as e:
            return [{"Error":"An error occurred"}]

    def get_department_by_name(self,name):
        try:
            department = self.__collection_dep.find_one({"Name":name})
            return department
        except Exception as e:
            return {"Error":"An error occurred"}

    def get_one_department(self,id):
        try:
            department = self.__collection_dep.find_one({"_id":ObjectId(id)})
            return department
        except Exception as e:
            return {"Error":"An error occurred"}
    
    def update_department(self,id,obj):
        try:
            self.__collection_dep.update_one({"_id": ObjectId(id)},{"$set":obj})
            return [{"Success":"The department has been updated" }]
        except Exception as e:
            return [{"Error":"An error occurred - the department was not deleted" }]


    def delete_all_departments(self):
        try:
            self.__collection_dep.delete_many({})
            return {"Success":"All departments have been deleted" }
        except Exception as e:
            return {"Error":"An error occurred The departments were not deleted" }

    def delete_manager_from_departments(self,managerId):
        obj = {"manager":''}
        try:
            self.__collection_dep.update_many({"manager":ObjectId(managerId)},{"$unset":obj})
            return [{"Success":"The manager was deleted from the department" }]
        except Exception as e:
            return [{"Error":"An error occurred - the manager was not deleted from the department" }]

    def create_new_department(self,obj):
        try:
            result = self.__collection_dep.insert_one({"Name":obj["department_name"]}) 
            return [{"Success":"department created"}]
        except Exception as e:
            return [{"Error":"unable to create department"}]

    #**********Shifts*************

    def get_shifts(self):
        result_list = list()
        try:
            result_list = list(self.__collection_shift.find({}))
            return result_list
        except Exception as e:
            return [{"Error":"An error occurred - it is not possible to fetch shifts"}]
    
    def get_one_shift(self,id):
        try:
            shift = self.__collection_shift.find_one({"_id":ObjectId(id)})
            return shift
        except Exception as e:
            return {"Error":"An error occurred - unable to find the shift"}

    
    def update_shift(self,id,obj):
        try:
            self.__collection_shift.update_one({"_id": ObjectId(id)},{"$set":obj})
            return [{"Success":"The shift has been updated" }]
        except Exception as e:
            return [{"Error":"An error occurred - the shift was not updated" }]

    
    def add_new_shift(self,obj):
        try:
            self.__collection_shift.insert_one(obj)
            return  [{"Success":"created with id: {}".format(str(obj["_id"]))}] 
        except Exception as e:
            return [{"Error":"An error occurred - the shift was not added" }]


    #***********shift_emp**************

    def get_all_shift_emp(self):
        result_list = list()
        try:
            result_list = list(self.__collection_shiftemp.find({}))
            return result_list
        except Exception as e:
            return [{"Error":"An error occurred " }]

    def get_shift_emp_by_empId(self,id):
        try:
            shift_emp = [i for i in self.__collection_shiftemp.find({"empId":ObjectId(id)})] 
            return shift_emp
        except Exception as e:
            return [{"Error":"An error occurred"}]

    def create_new_shift_emp(self,empId, item):
        try:
            self.__collection_shiftemp.insert_one({"empId":ObjectId(empId),
            "shiftId":ObjectId(item)}) 
            return  {"Success":""}
        except Exception as e:
            return {"Error":"An error occurred" }
    
    def delete_shifts_of_emp(self,empId):
        try:
            self.__collection_shiftemp.delete_many({"empId":ObjectId(empId)})
            return [{"Success":"The employee's shifts have been deleted" }]
        except Exception as e:
            return [{"Error":"An error occurred - the employee's shifts were not deleted" }]

# **************************user*****************************
    def get_all_users(self):
        result_list = list()
        result_list = list(self.__collection_users.find({}))
        return result_list

    
    def user_exist(self,field_name,field_value):
        if field_name == "_id":
            field_value = ObjectId(field_value)
        try:
            user = self.__collection_users.find_one({field_name:field_value})
            return user
        except Exception as e:
            return {"Error":"An error occurred" }
