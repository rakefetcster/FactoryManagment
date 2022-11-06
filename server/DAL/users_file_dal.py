import json
import os
import sys
from json.decoder import JSONDecodeError

class UsersFileDal:
    def __init__(self):
        self.__path = os.path.join(sys.path[0],'data/users.json')

    def read_file(self):
        with open(self.__path,'r') as f:
            try:
                data = json.load(f)
                return data
            except JSONDecodeError:
                return []
        
    
    def write_file(self,data):
        with open(self.__path,'w') as f:
            json.dump(data,f)
