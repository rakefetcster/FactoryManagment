from flask import Flask
import json
from bson import ObjectId
from flask_cors import CORS
from ROUTERS.employee_router import emp
from ROUTERS.department_router import dep
from ROUTERS.shift_router import shi
from ROUTERS.shift_emp_router import shi_emp
from datetime import date, datetime
from ROUTERS.auth_routher import auth
from ROUTERS.user_router import users

class JSONEncoder(json.JSONEncoder):
    def default(self, obj) :
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self,obj)

app = Flask(__name__)
app.json_encoder = JSONEncoder
app.url_map.strict_slashes = False
CORS(app)
app.register_blueprint(emp, url_prefix="/employee")
app.register_blueprint(shi_emp, url_prefix="/shift_emp")
app.register_blueprint(dep, url_prefix="/department")
app.register_blueprint(shi, url_prefix="/shift")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(users, url_prefix="/user")


app.run()