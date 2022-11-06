from DAL.factory_db_dal import FactoryDBDal

class ShiftEmp:
    def __init__(self):
        self.__factory_db_dal=FactoryDBDal()

    def get_all_shift_emp(self):
        obj_list = list()
        shift_emp_from_db = self.__factory_db_dal.get_all_shift_emp()
        for shiftEmp in shift_emp_from_db:
            if "Error" in shiftEmp:
                return shift_emp_from_db
            obj_list.append({
                "empId":shiftEmp["empId"],
                "shiftId":shiftEmp["shiftId"]
            })
        return obj_list


    def create_new_shiftEmp(self,obj):
        shift_list = list()
        result = self.__factory_db_dal.delete_shifts_of_emp(obj["empId"])
        for res in result:
            if "Error" in res:
                return result
        for item in obj["shiftId"]:
            if item not in shift_list:
                result = self.__factory_db_dal.create_new_shift_emp(obj["empId"],item)
                if "Error" in result:
                    return result
        return [{"Success":"created"}]
