from peewee import *
db = SqliteDatabase('cadastro.db')

class Usuario(Model):
    nome = CharField()
    email = CharField(unique=True)
    senha = CharField()

    class Meta:
        database=db

class Projeto(Model):
     nome_projeto = CharField()

     class Meta:
         database = db

