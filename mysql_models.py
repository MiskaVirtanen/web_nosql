import mysql.connector

conn = mysql.connector.connect(host="localhost",user="root", passwd="usbw",db="test")


class User:
    def __init__(self, username, _id=None):
        self.username = username
        self._id = _id

    def create(self):
        
        try:
            query = f"INSERT INTO users (username) VALUES (?)"
            cursor = conn.cursor(prepared=True)
            cursor.execute(query, (self.username,))
            conn.commit()
            self.id = cursor.lastrowid
            cursor.close()
            
        except Exception as ex:
            print(ex)
            conn.rollback()
            raise ex
    
    def update(self):
        try:
            query = f"UPDATE users SET username = ? WHERE id = ?"
            cursor = conn.cursor(prepared=True)
            cursor.execute(query, (self.username, self._id))
            conn.commit()
            cursor.close()
        except Exception as ex:
            conn.rollback()
            raise ex
    
    @staticmethod
    def get_by_id(_id):
        query = "SELECT * FROM users WHERE id = ?"
        cursor = conn.cursor(prepared=True)
        cursor.execute(query, (_id,))
        user = cursor.fetchone()
        return User(user[1], _id=user[0])

        
    @staticmethod
    def get_all():
        users = []
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        for u in cursor.fetchall():
            users.append(User(u[1], _id=u[0]))
        cursor.close()
        
        return users
    
    @staticmethod
    def delete_by_id(_id):
        try:
            query = "DELETE FROM users WHERE id = ?"
            
            cursor = conn.cursor(prepared=True)
            cursor.execute(query, (_id, ))
            conn.commit()
        except Exception as ex:
            conn.rollback()
            raise ex
    
    def to_json(self):
        return {
            '_id': self._id,
            'username': self.username
        }
    
    @staticmethod
    def list_to_json(user_list):
        users = []
        for user in user_list:
            users.append(user.to_json())
        return users


        
    
        
        
        





