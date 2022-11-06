import requests

class UserWSDal:
    def __init__(self):
        self.__url = "https://jsonplaceholder.typicode.com/users"

    def get_one_user(self,username):
        resp = requests.get(self.__url+"?name="+username)
        return resp.json()