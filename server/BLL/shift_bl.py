from DAL.factory_db_dal import FactoryDBDal
from datetime import date,datetime

class ShiftBL:
    def __init__(self):
        self.__factory_db_dal=FactoryDBDal()
   
    def get_shifts(self,user_fullName):
        result_list = list()
        shifts_from_db = self.__factory_db_dal.get_shifts()
        for data in shifts_from_db:
            if "Error" in data:
                return shifts_from_db
            date = str(data["date"].day)+"/"+str(data["date"].month)+"/"+str(data["date"].year)
            result_list.append({
                "id":data["_id"],
                "Date":date,
                "StartingHour":data["starting_hour"],
                "EndingHour":data["ending_hour"],
                "user_name":user_fullName
            })

        return result_list


    def get_one_shift(self,id):
        shift_db = self.__factory_db_dal.get_one_shift(id)
        if "Error" in shift_db:
            return [shift_db]
        date = str(shift_db["date"].day)+"/"+str(shift_db["date"].month)+"/"+str(shift_db["date"].year)
        obj = { "id":shift_db["_id"],
                "Date":date,
                "StartingHour":shift_db["starting_hour"],
                "EndingHour":shift_db["ending_hour"]}
        return obj


    def update_this_shift(self,id,obj):
        date_list = obj["date"].split("/")
        date = datetime(int(date_list[2]), int(date_list[1]), int(date_list[0]))
        new_obj = {"date":date,
                "starting_hour": obj["starting_hour"],
                "ending_hour":obj["ending_hour"] }
        result = self.__factory_db_dal.update_shift(id,new_obj)
        return  result

    def create_new_shift(self,obj):
        date_list = obj["date"].split("/")
        date = datetime(int(date_list[2]), int(date_list[1]), int(date_list[0]), 0, 0)
        
        new_obj = {"date":date,
                "starting_hour": obj["starting_hour"],
                "ending_hour":obj["ending_hour"] }
        result = self.__factory_db_dal.add_new_shift(new_obj)
        return result