import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #SECRET_KEY = "dev-secret-key"

    #SQLALCHEMY_DATABASE_URI = "sqlite:///property_manager.db"
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "change-this-to-a-randon-secret-key"
    SQLALCHEMY_DATABASE_URI = \
        "sqlite:///" + os.path.join(basedir, "instance", "property_manager.db") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
