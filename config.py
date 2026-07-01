import os


class Config:
    SECRET_KEY = "dev-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///property_manager.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False