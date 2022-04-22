from flask import request


from models import User

# api/register
# tänne pääsee kirjautumatta kuka vaan, koska kyse on uuden käyttäjätilin luonnista
def register_route_handler():
    if request.method == 'POST':
        # otetaan insomniasta lähetetty data talteen
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
        user = User(username, password=password)
        user.create()
        return ""