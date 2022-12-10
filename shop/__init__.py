from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os


basedir = os.path.abspath(os.path.dirname(__file__))
# create the app
app = Flask(__name__)


# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db' 

# configure Bcrypt to encrypt for password
app.config['SECRET_KEY'] = 'ajdjf0sfdfsd'
bcrypt = Bcrypt(app)

# configure for app upload
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)



# create the extension
db = SQLAlchemy(app)
db.init_app(app)


from shop.admin import routes
from shop.products import routes