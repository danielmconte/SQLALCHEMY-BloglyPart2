from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url = {u.image_url}>"

    id = db.Column(db.Integer,
    				primary_key=True,
    				autoincrement=True)
    first_name = db.Column(db.String(10),
    						nullable=False,
    						unique=True)

    last_name = db.Column(db.String(10),
    						nullable=False)

    image_url = db.Column(db.String(500)) 

    


class Post(db.Model):

    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at = {p.created_at} id_code = {p.id_code}>"

    id = db.Column(db.Integer,
    			    primary_key=True,
    				autoincrement=True)
    title = db.Column(db.String(20),
                        nullable=False,
                        unique=True)
    content = db.Column(db.String(200),
                        nullable=False)
    created_at = db.Column(db.String) 
    
    id_code = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref = 'posts')

    tags = db.relationship('Tag', secondary="posttags", backref="posts")

class Tag(db.Model):

    __tablename__='tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False, unique=True)


class PostTag(db.Model):
    __tablename__='posttags'

    post_id =db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
     






