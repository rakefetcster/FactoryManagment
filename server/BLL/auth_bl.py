from urllib import request
from DAL.factory_db_dal import FactoryDBDal
from DAL.users_dal import UserWSDal
import jwt

class AuthBL:
    def __init__(self):
        self.__factory_db_dal=FactoryDBDal()
        self.__user_dal=UserWSDal()
        self.__key = "server_key"
        self.__algorithm = "HS256"

    def get_token(self,username, email):
        user_id = self.__check_user(username,email)
        token = None
        if "Error" not in user_id:
            token = jwt.encode({"userid" : user_id}, self.__key, self.__algorithm)
        return token

    def verify_token(self, token):
        data = jwt.decode(token, self.__key, self.__algorithm)
        user_id = data["userid"]
        userObj = self.__factory_db_dal.user_exist("_id",user_id)
        if userObj != None: 
            if "Error" in userObj:
                return False
            return True,userObj
        return False


    def __check_user(self,username, email):
        # Check existance of that user in data base....
        user_list = self.__user_dal.get_one_user(username)
        if user_list != []:
            for user in user_list:
                if user["email"] == email:
                    user_obj = self.__factory_db_dal.user_exist("FullName",username)
                    if user_obj != []:
                        if "Error" in user_obj:
                            return user_obj
                        return str(user_obj["_id"])
        return {"Error":"Unauthorized user"}
