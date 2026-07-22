import os


class Config:

    SECRET_KEY = "babybloom-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///babybloom.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False