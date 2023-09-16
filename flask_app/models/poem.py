from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

# ***** ATTENTION: Pending DB name. Modify after creating DB ("poems_schema" for now...)******
class Poem:
    DB = "poems_schema"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.genre=data['genre']
        self.poem_text=data['poem_text']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user=None
        
    @classmethod
    def save(cls,data):
        query = """INSERT INTO poems (title,author,genre,poem_text)
                VALUES (%(title)s,%(author)s,%(genre)s,%(poem_text)s,%(user_id)s);"""
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM poems JOIN users on poems.user_id = users.id;"""
        results = connectToMySQL(cls.db_name).query_db(query)
        poems = []
        for poem_dict in results:
            poem_obj = Poem(poem_dict)
            
            user_obj = user.User({
                "id": poem_dict['users.id'],
                "first_name": poem_dict['first_name'],
                "last_name": poem_dict['last_name'],
                "email": poem_dict['email'],
                "created_at": poem_dict['users.created_at'],
                "updated_at": poem_dict['users.updated_at']
            })
            
            poem_obj.user = user_obj
            poems.append(poem_obj)
        return poems
        
    @classmethod
    def update(cls,data):
        query = """UPDATE poems
                SET title = %(title)s,
                author = %(author)s,
                genre = %(genre)s ,
                poem_text = %(poem_text)s,
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db_name).query_db(query,data)
        
# Get by ID

# Validate

    @classmethod
    def delete(cls,data):
        query = """DELETE FROM poems WHERE id = %(id)s;"""
        return connectToMySQL(cls.db_name).query_db(query,data)