# tässä on MCV: osa C eli controller

from flask import Flask, jsonify
from controllers.account_controller import AccountRouteHandler
from controllers.login_controller import login_route_handler
from controllers.publications_controller import publications_route_handler
from controllers.register_controller import register_route_handler

from controllers.users_controller import user_route_handler, users_route_handler
from flask_jwt_extended import JWTManager

from errors.not_found import NotFound



# Flask(__name__) merkitys selviää, kun päästään luokkiin asti
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



# __name__-muuttujan arvo riippuu siitä, miten app.py suoritetaan
# kun app.py suoritetaan python app.py kommennolla, __name__-muuttujan arvo on __main__
# kun app.py importataan, sen nimeksi tulee app, eli skriptin nimi

# jos ao. ehtoa ei olisi, flask web-serveri käynnistyisi aina, kun app.py importataan toiseen
# tiedostoon

# se, mitä @-merkki tekee, selviää myöhemmin
if __name__ == '__main__':
    # kun debug-muuttujan arvo on True, palvelin käynnistyy aina itsestään uudelleen
    # kun koodi muuttuu. Tämä on kätevää kehitysvaiheessa
    app.run(debug=True)
    

