from flask import request


from models import User

def register_route_handler():
    if request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
        user = User(username, password=password)
        user.create()
        return ""