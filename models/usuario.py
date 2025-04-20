from peewee import CharField, Model
from models.banco import db

class Usuario(Model):
    nome = CharField()
    email = CharField(unique=True)
    senha = CharField()

    class Meta:
        database=db
 

