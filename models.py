import random
import string
import pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256 as sha256
from config import Config
from errors.not_found import NotFound
from errors.not_found import NotFound

client = pymongo.MongoClient("mongodb+srv://miskavirtanen:atikV123@miskavirtanen.kbont.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
server_api=ServerApi('1')
db = client.group1



class Publication:
    def __init__(
        self, 
        title, 
        description, 
        url,
        owner=None, 
        likes=[],
        shares=0,
        share_link=None,
        comments=[],
        visibility=2,  
        _id=None

    ):
        self.title = title
        self.description = description
        self.url = url
        self.owner = owner
        self.likes = likes
        self.shares = shares
        self.share_link = share_link
        self.comments = comments
        self.visibility = visibility
        if _id is not None:
            _id = str(_id)
        self._id = _id
    
    @staticmethod
    def get_by_visibility(visibility=2):
        _filter = {
            'visibility': visibility
        }
        publications = []
        publications_cursor = db.publications.find(_filter)
        for publication in publications_cursor:

            title = publication['title']
            description = publication['description']
            url = publication['url']
            owner = publication['owner']
            likes = publication['likes']
            shares = publication['shares']
            share_link = publication['share_link']
            comments = publication['comments']
            visibility = publication['visibility']
            _id = publication['_id']
            
            publication_object = Publication(title, 
            description, 
            url, 
            owner=owner, 
            likes=likes,
            shares=shares,
            share_link=share_link,
            comments=comments,
            visibility=visibility,
            _id=_id)

            publications.append(publication_object)
        
        return publications

    def delete(self):
        db.publications.delete_one({'_id': ObjectId(self._id)})


    @staticmethod
    def delete_by_id(_id):
        db.publications.delete_one({'_id': ObjectId(_id)})

    def like(self):
        _filter={'_id': ObjectId(self._id)}
        _update= {'$set': {'likes': self.likes}}
        db.publications.update_one(_filter, _update)

    def share(self, length):
        if self.share_link is None:
            letters = string.ascii_lowercase
            self.share_link = ''.join(random.choice(letters) for i in range (length))
            _filter={'_id': ObjectId(self._id)}
            _update= {'$set': {'share_link': self.share_link}}
            db.publications.update_one(_filter, _update)

            
    @staticmethod
    def get_by_id(id):
        _filter = {
            'visibility': visibility
        }
        publications = []
        publications_cursor = db.publications.find(_filter)
        for publication in publications_cursor:

            title = publication['title']
            description = publication['description']
            url = publication['url']
            owner = publication['owner']
            likes = publication['likes']
            shares = publication['shares']
            share_link = publication['share_link']
            comments = publication['comments']
            visibility = publication['visibility']
            _id = publication['_id']
            
            publication_object = Publication(title, 
            description, 
            url, 
            owner=owner, 
            likes=likes,
            shares=shares,
            share_link=share_link,
            comments=comments,
            visibility=visibility,
            _id=_id)

            publications.append(publication_object)
        
        return publications 


    
    @staticmethod
    def get_by_owner_and_visibility(user={}, visibility=[2]):
        _filter = {
            '$or': [
                {'owner': ObjectId(user['sub'])},
                {'visibility': {'$in': visibility}}

            ]
        }
        publications = []
        publications_cursor = db.publications.find(_filter)
        for publication in publications_cursor:

            title = publication['title']
            description = publication['description']
            url = publication['url']
            owner = publication['owner']
            likes = publication['likes']
            shares = publication['shares']
            share_link = publication['share_link']
            comments = publication['comments']
            visibility = publication['visibility']
            _id = publication['_id']
            
            publication_object = Publication(title, 
            description, 
            url, 
            owner=owner, 
            likes=likes,
            shares=shares,
            share_link=share_link,
            comments=comments,
            visibility=visibility,
            _id=_id)

            publications.append(publication_object)
        
        return publications 
    
    @staticmethod
    def list_to_json(publications_list):
        publications_in_json_fomat = []
        for publication_object in publications_list:
            publication_object_in_json_format = publication_object.to_json()
            publications_in_json_fomat.append(publication_object_in_json_format)
        
        return publications_in_json_fomat

    
    @staticmethod
    def get_all():
        publications = []
        publications_cursor = db.publications.find()
        for publication in publications_cursor:

            title = publication['title']
            description = publication['description']
            url = publication['url']
            owner = publication['owner']
            likes = publication['likes']
            shares = publication['shares']
            share_link = publication['share_link']
            comments = publication['comments']
            visibility = publication['visibility']
            _id = publication['_id']
            
            publication_object = Publication(title, 
            description, 
            url, 
            owner=owner, 
            likes=likes,
            shares=shares,
            share_link=share_link,
            comments=comments,
            visibility=visibility,
            _id=_id)
            publications.append(publication_object)

        return publications


    
    def create(self):
        title = self.title
        description = self.description
        url = self.url
        owner = self.owner
        likes = self.likes
        shares = self.shares
        share_link = self.share_link
        comments = self.comments
        visibility = self.visibility
        result = db.publications.insert_one({
            'title': title,
            'description': description,
            'url': url,
            'owner': owner,
            'likes': likes,
            'shares': shares,
            'share_link': share_link,
            'comments': comments,
            'visibility': visibility
        })
        new_id = result.inserted_id
        self._id = str(new_id)
        
        

        
        
    
    def to_json(self):
        owner = self.owner
        if owner is not None:
            owner = str(owner)
        likes = self.likes
        for user in likes:
            user = str(user)
        publication_in_json_format = {
            '_id': str(self._id),
            'title': self.title,
            'description': self.description,
            'owner':owner,
            'shares': self.shares,
            'likes': likes,
            'share_link': self.share_link,
            'visibility': self.visibility,
            
        }

        return publication_in_json_format
        

class User:
    def __init__(self, username, password=None, role='user', _id=None):
        self.username = username
        self.password = password
        self.role = role
        
        if _id is not None:
            _id = str(_id)
        self._id = _id
    
    @staticmethod
    def get_by_username(username):
        user = db.users.find_one({'username': username})
        if user is None:
            raise NotFound(message='User not found')
        return User(username, 
        password=user['password'], 
        role=user['role'], 
        _id=user['_id'])
    
    
    def update(self):
        db.users.update_one(
            {'_id': ObjectId(self._id)}, {
            '$set': {'username': self.username}
        })
    def create(self):
        # TODO:
        result = db.users.insert_one({'username': self.username, 
        'password': sha256.hash(self.password), 'role': self.role})
        self._id = str(result.inserted_id)
    
    
        

    @staticmethod
    def get_all():
        
        users = []
        users_cursor = db.users.find()
        for user in users_cursor:
            users.append(User(user['username'], _id=str(user['_id'])))
        return users
    

    @staticmethod
    def delete_by_id(_id):
        db.users.delete_one({'_id': ObjectId(_id)})

    @staticmethod
    def get_by_id(_id):
        user = db.users.find_one({'_id': ObjectId(_id)})
        if user is None:
            raise NotFound(message='User not found')
        return User(user['username'], _id=str(user['_id']))

    def delete(self):
        db.users.delete_one({'_id': ObjectId(self._id)})

    
    @staticmethod
    def list_to_json(user_list):
        json_list = []
        for user in user_list:
            user_in_json_format = user.to_json()
            json_list.append(user_in_json_format)
        return json_list
    
    def to_json(self):
        user_in_json_format = {
            '_id': str(self._id),
            'username': self.username,
            'role': self.role
        }
        return user_in_json_format




    
    









