from DAL.factory_db_dal import FactoryDBDal
from DAL.users_file_dal import UsersFileDal
from datetime import date
from BLL.auth_bl import AuthBL


class UserBL:
    def __init__(self):
        self.__factory_db_dal=FactoryDBDal()
        self.__users_file_dal = UsersFileDal()

    def get_users(self, user_fullName):
        max_action = 0
        obj_list = list()
        all_users = self.__factory_db_dal.get_all_users()
        for usreObj in all_users:
            max_action = self.read_data_from_file(usreObj)
            obj_list.append({
                "id":usreObj["_id"],
                "FullName":usreObj["FullName"],
                "maxAction": int(usreObj["NumOfAction"]),
                "currentAction": int(max_action),
                "user_name":user_fullName
            })
        return obj_list

    def get_user_name(self,id):
        userObj = self.__factory_db_dal.user_exist("_id",id)
        return {"user_name":userObj['FullName'] }

    def read_data_from_file(self, userObj):
        today = date.today()
        today_date = today.strftime("%d/%m/%Y")
        max_action = 0
        all_data = self.__users_file_dal.read_file()
        if all_data != []:
            for row in all_data["actions"]:
                if row["id"] == str(userObj["_id"]):
                    if str(row["date"]) == str(today_date):
                        max_action = int(row["maxActions"])
        return max_action

    def add_row_to_file(self,userObj,max_action):
        today = date.today()
        today_date = today.strftime("%d/%m/%Y")
        all_data = self.__users_file_dal.read_file()
        row_to_add = {"id":str(userObj["_id"]),"maxActions":max_action,
                    "date":today_date,"ActionAllowd":int(userObj["NumOfAction"])}
        if all_data == []:
            all_data = {"actions":[row_to_add]}
        else:
           all_data["actions"].append(row_to_add)
        self.__users_file_dal.write_file(all_data)


    def check_user(self,token):
        today = date.today()
        today_date = today.strftime("%d/%m/%Y")
        auth_BL = AuthBL()
        exist,userObj = auth_BL.verify_token(token)
        max_action = 0
        autorized = True
        if exist == True:
            max_action = self.read_data_from_file(userObj)
            if int(max_action) >= int(userObj["NumOfAction"]):
                autorized = False   
                exist = False
            else:
                max_action = int(max_action)+1
                self.add_row_to_file(userObj,max_action)
        return exist,userObj["FullName"],autorized

    
    