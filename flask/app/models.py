from app import db1, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user = User.getUser(str(user_id))
    return user

class User(UserMixin):
    id = ''
    username = ''
    name = ''
    password = '' 

    def __init__(self, user_id, name):
        self.id = user_id 
        self.username = user_id 
        self.name = name

    def getUser(user_id):
        user =  db1.child('Users').child(user_id).get().val()
        if user == None: 
            return None
        else:
            usr = User(user_id, user.get('name'))
            return usr
        
    def __repr__(self):
        return f"User('{self.username}', '{self.name}')"

class FireBaseUtil():

    def getUserPassword(id):
        return db1.child('Users').child(id).get().val().get('Password') 

    def getUser(id):
        user =  db1.child('Users').child(id).get().val()
        return {"user_id": user.get('Password'), "name": user.get('name')} 
    
    def createPost(title, content, name, username):

        ref = db1.child('Posts').push({"id":'temp', "title":title, "content":content, "name":name, "user_id":username})
        db1.child('Posts').child(ref.get('name')).update({"id":ref.get('name')})
        

    def updatePost (title, content,post):

        db1.child('Posts').child(post.get('id')).update({"title":title, "content":content})
        
        
    def getAllPosts():
        posts = []
        raw_posts = db1.child('Posts').get().each()
        if raw_posts == None:
            return [{"author":{"username":"rkallem", "name":"Deekshith Reddy Kallem"}, "id":"123", "title":"No Posts!", "content":"Add new posts! Go to www.doosratake.com/post/new"}]

        for post in db1.child('Posts').get().each():
            posts.append({"author":{"username":post.val().get('user_id'), "name":post.val().get('name')}, "id":post.val().get('id'), "title":post.val().get('title'), "content":post.val().get('content')})
        return posts

    def getPost(id):
        post = db1.child('Posts').child(id).get()
        return {"author":{"username":post.val().get('user_id'),"name":post.val().get('name')}, "id":post.val().get('id'), "title":post.val().get('title'), "content":post.val().get('content')}

    def removePost(id):
        db1.child("Posts").child(id).remove()
