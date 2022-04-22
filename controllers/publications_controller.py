
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from bson.objectid import ObjectId

from models import Publication

@jwt_required(optional=True)
def publications_route_handler():
    logged_in_user = get_jwt()
    if request.method == 'GET':
        if logged_in_user: # jos on kirjauduttu sisään
            if logged_in_user['role'] == 'admin':
                publications = Publication.get_all()
            elif logged_in_user['role'] == 'user':
                # haetaan kaikki omat + ne joissa visibility = 1 tai 2
                publications = Publication.get_by_owner_and_visibility(user=logged_in_user, visibility=[1,2])
        
        else: # käyttäjä ei ole kirjautunut sisään
            publications = Publication.get_by_visibility(visibility=2)

        publications_in_json_format = Publication.list_to_json(publications)
        return jsonify(publications=publications_in_json_format)
        
    elif request.method == 'POST':
        owner = None
        if logged_in_user:
            owner = ObjectId(logged_in_user['sub'])
        request_body = request.get_json()
        title = request_body['title']
        description = request_body['description']
        visibility = request_body.get('visibility', 2)
        url = request_body['url']
        new_publication = Publication(title, description, url, visibility=visibility, owner=ObjectId(owner))
        new_publication.create()
        
        return jsonify(publication=new_publication.to_json())