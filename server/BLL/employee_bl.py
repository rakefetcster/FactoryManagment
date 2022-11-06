from asyncio.windows_events import NULL
from DAL.factory_db_dal import FactoryDBDal
from datetime import date

class Employee:
    def __init__(self):
        self.__factory_db_dal=FactoryDBDal()

    def get_all_employee(self,user_fullName):     
        employee_from_db = self.__factory_db_dal.get_all_employee()
        emp_list = list()
        for employee in employee_from_db:
            if "Error" in employee:
                return employee_from_db
            else:
                shift_list = list()
                emp_dict = dict()
                shift_emp = ''
                if "departmentId" in employee:
                    department = self.__factory_db_dal.get_one_department(employee["departmentId"])
                    
                    emp_dict.update({"departmentId": employee["departmentId"]})
                    if "Error" in department:
                        return [department]
                    elif department != None:
                        emp_dict.update({"Department":department["Name"]})  
                shift_emp = self.__factory_db_dal.get_shift_emp_by_empId(employee["_id"])       
                for shiftId in shift_emp:
                    if "Error" in shiftId:
                        return [shiftId]
                    this_shift = self.__factory_db_dal.get_one_shift(shiftId["shiftId"])
                    if "Error" in this_shift:
                        return [this_shift]
                    date = str(this_shift["date"].day)+"/"+str(this_shift["date"].month)+"/"+str(this_shift["date"].year)
                    shift_list.append({
                        "id": this_shift["_id"],
                        "date":date,
                        "starting_hour":this_shift["starting_hour"],
                        "ending_hour":this_shift["ending_hour"]
                    })
                emp_dict.update({
                    "id": employee["_id"],
                    "FirstName": employee["FirstName"],
                        "LastName" : employee["LastName"],
                        "StartWorkYear":employee["StartWorkYear"],
                        "shifts":shift_list,
                        "user_name":user_fullName
                        
                        })
                emp_list.append(emp_dict)
        return emp_list
        
    
    def get_employee_by_id(self,id):
        dep_name = ''
        emp_dict = dict()
        shift_list = list()
        employee = self.__factory_db_dal.get_one_employee(id)
        if "Error" in employee:
            return [employee]
        if "departmentId" in employee:
            department = self.__factory_db_dal.get_one_department(employee["departmentId"])
            if "Error" in department:
                return [department]
            elif department != None:
                emp_dict.update({"Department": str(department["Name"])})
            emp_dict.update({"departmentId":employee["departmentId"]})
        shift_emp = self.__factory_db_dal.get_shift_emp_by_empId(employee["_id"])       
        for shiftId in shift_emp:
            shift_list.append(self.__factory_db_dal.get_one_shift(shiftId["shiftId"]))
        emp_dict.update({
                "id": employee["_id"],
                "FirstName": employee["FirstName"],
                    "LastName" : employee["LastName"],
                    "StartWorkYear":employee["StartWorkYear"],
                    "shifts":shift_list
                    })
        return emp_dict
    
    def add_new_employee(self,empObj):
        obj_dict = dict()
        dep_obj = self.__factory_db_dal.get_department_by_name(empObj["department_name"])
        if dep_obj == None:
            return [{"Error": "The employee was not created - the department name is missing or the employee already exists in the system"}]
        elif "Error" in dep_obj:
            return [dep_obj]
        
        else:
            obj_dict = {"FirstName":empObj["first_name"],
                        "LastName": empObj["last_name"],
                        "StartWorkYear": date.today().year,
                        "departmentId":dep_obj["_id"]
                        }
            employee_from_db = self.__factory_db_dal.get_all_employee()
            for emp in employee_from_db:
                if "Error" in emp:
                    return [emp]
                elif emp["FirstName"]==obj_dict["FirstName"] and emp["LastName"]==obj_dict["LastName"]:
                    return [{"Error": "There is an employee with the same name"}]
                    break

            result = self.__factory_db_dal.insert_new_employee(obj_dict)
            return result

    def update_employee(self,id,obj):
        if "shifts" in obj:
            result = self.update_emp_shift(id,obj)
            if "Error" in result:
                return result
        dep_id = ''
        new_obj = dict()
        res = False
        this_id_list = list()
        if "departmentName" in obj:
            department = self.__factory_db_dal.get_all_departments()
            for dep in department:
                if "Error" in dep:
                    return dep
                elif str(dep["Name"]) == obj["departmentName"]:
                    res = True
                    obj["departmentId"] = str(dep["_id"])
                    break

        elif "department" in obj:
            department = self.__factory_db_dal.get_all_departments()
            for dep in department:
                if "Error" in dep:
                    return dep
                if str(dep["_id"]) == obj["department"]:
                    res = True
                    obj["departmentId"] = str(dep["_id"])
                    break
        if res:
            result = self.__factory_db_dal.update_employee(id,obj)
            return result
        else:        
            return [{"Error":" The department was not created - the employee cannot be updated"}]

    def update_emp_shift(self,id,obj):
        if len(obj["shifts"])==0:
            result = self.__factory_db_dal.insert_shift_to_emp(id,obj["shifts"])
            return result
        if len(obj["shifts"]) == 1:
            this_id =obj["shifts"][0] 
            result = self.__factory_db_dal.insert_shift_to_emp(id,this_id)
        elif len(obj["shifts"]) > 1:
            for shiftId in obj["shifts"]:
                result = self.__factory_db_dal.insert_all_shift(id,shiftId)
                if "Error" in result:
                    return result
                
     
    def delete_employee(self,id):
        result_str=''
        #delete the shifts
        result1 = self.__factory_db_dal.delete_shifts_of_emp(id)
        #delete the manager from the department
        result2 = self.__factory_db_dal.delete_manager_from_departments(id)
        #delete employee
        result = self.__factory_db_dal.delete_this_employee(id)
        for res in result:
            if "Error" in res:
                return result  
            else:
                result_str += res["Success"]+"-"
        for res in result1:
            if "Error" in res:
                return result1 
            else:
                result_str += res["Success"]+"-"
        for res in result2:
            if "Error" in res:
                return result2 
            else:
                result_str += res["Success"]    
        return [{"Success":result_str}]