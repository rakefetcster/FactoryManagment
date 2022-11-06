from DAL.factory_db_dal import FactoryDBDal

class DepartmentBl:
    def __init__(self):
        self.__factory_db_dal=FactoryDBDal()

    def get_departments(self,user_fullName):
        departments_from_db = self.__factory_db_dal.get_all_departments()
        dep_list = list()
        for department in departments_from_db:
            if "Error" in department.keys():
                return [department]
            emp_list = list()
            dep_dict = dict()
            if "manager" in department.keys():
                manager = ''
                manager = self.__factory_db_dal.get_one_employee(str(department["manager"]))
                if manager != None:
                    if "Error" in manager:
                        return manager
                    dep_dict.update({"manager":manager["FirstName"]+"-"+manager["LastName"]})
            # employes = self.get_all_employees_by_department(department["_id"])
            employes=self.__factory_db_dal.get_employees_by_department_id(department["_id"])
            for employe in employes:
                if "Error" in employe:
                    return employe
                if employe["_id"] not in emp_list:
                    emp_list.append({"id":employe["_id"],
                                    "FirstName":employe["FirstName"],
                                    "LastName":employe["LastName"]})
            dep_dict.update({"EmployeesList":emp_list})
            dep_dict.update({
                "id": department["_id"],
                "Name": department["Name"],
                "user_name":user_fullName })
            dep_list.append(dep_dict)
        return dep_list

    # def get_all_employees_by_department(self,id):
    #     employees_from_db=self.__factory_db_dal.get_employees_by_department_id(id)
    #     return employees_from_db

    def get_department_id(self,id):
        dep_dict = dict()
        the_manager = ''
        managerId = ''
        department = self.__factory_db_dal.get_one_department(id)
        if "Error" in department.keys():
            return [department]
        elif "manager" in department.keys():
            manager = self.__factory_db_dal.get_one_employee(department["manager"])
            if "Error" in manager:
                return [manager]
            dep_dict.update({"manager":manager["FirstName"]+"-"+manager["LastName"]}) 
            dep_dict.update({"managerId":manager["_id"]}) 
            managerId =manager["_id"]
        dep_dict.update({"id":department["_id"],
                    "Name": department["Name"]})
        return dep_dict

    def update_department_by_id(self,id,obj):
        objDep = dict()
        result = [{"Error":"The department has not been updated"}]
        objEmp = dict()
        manager_name_list = obj["manager"].split("-")
        objEmp.update({"FirstName": manager_name_list[0],
                    "LastName": manager_name_list[1]})
        objDep.update({"Name": obj["name"]})
        employees = self.__factory_db_dal.get_all_employee()
        for emp in employees:
            if "Error" in emp:
                return [emp]
            if objEmp["FirstName"] == emp["FirstName"] and objEmp["LastName"] == emp["LastName"]:
                objDep.update({"manager":emp["_id"]})
                result = self.__factory_db_dal.update_employee(emp["_id"],{"departmentId":id})
                for res in result:
                    if "Error" in res:
                        return result
                result = self.__factory_db_dal.update_department(id,objDep)
                for res in result:
                    if "Error" in res:
                        return result
                return result
        
        return result
        
        
    def deletet_department_by_id(self,obj):
        result = self.__factory_db_dal.delete_one_field_from_emp(obj)
        if "Error" in result.keys():
            return [{"Error": "An error occurred - the departments were not deleted - the field in the employee was not deleted"}]
        else:
            result = self.__factory_db_dal.delete_all_departments()
            if "Error" in result.keys():
                return result
        return [{"Success": "All departments have been deleted"}]
    
    def add_new_department(self,obj):
        departments_from_db = self.__factory_db_dal.get_all_departments()
        for department in departments_from_db:
            if "Error" in department:
                return [department]
            if department["Name"] == obj["department_name"]:
                return [{"Error": "The department was not created - the department name already exists"}]
                break
        result = self.__factory_db_dal.create_new_department(obj)
        return result




