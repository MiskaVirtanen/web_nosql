from flask import Flask, jsonify
from controllers.account_controller import AccountRouteHandler
from controllers.login_controller import login_route_handler
from controllers.publications_controller import like_publication_route_handler, publications_route_handler, share_publication_route_handler
from controllers.register_controller import register_route_handler
from controllers.users_controller import user_route_handler, users_route_handler
from flask_jwt_extended import JWTManager
from errors.not_found import NotFound

app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)

@app.errorhandler(NotFound)
def handle_not_found(err):
    return jsonify(err=err.args), 404

app.add_url_rule('/api/users', view_func=users_route_handler, methods=['GET', 'POST'])
app.add_url_rule('/api/users/<_id>', view_func=user_route_handler, methods=['GET', 'DELETE', 'PATCH'])
app.add_url_rule('/api/register', view_func=register_route_handler, methods=['POST'])
app.add_url_rule('/api/login', view_func=login_route_handler, 
methods=['POST'])

app.add_url_rule('/api/account', view_func=AccountRouteHandler.as_view('account_route_handler'))

app.add_url_rule('/api/publications', view_func=publications_route_handler, methods=['GET', 'POST'])

app.add_url_rule('/api/publications/<_id>/like', view_func=like_publication_route_handler, methods=['PATCH'])
app.add_url_rule('/api/publications/<_id>/share', view_func=share_publication_route_handler, methods=['PATCH'])

if __name__ == '__main__':
    app.run(debug=True)
    

