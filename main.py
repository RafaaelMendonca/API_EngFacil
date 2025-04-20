from flask import Flask
from models.banco import db
from models.usuario import Usuario

app = Flask(__name__)

# SEMPRE IMPORTAR APÓS O APP
from routes.route import *

def inicializar_tabelas():
    db.create_tables([Usuario], safe=True)
    print("Tabelas criadas com sucesso!")

@app.before_request
def before_request():
    if db.is_closed():
        db.connect()

@app.teardown_request
def teardown_request(exception):
    if not db.is_closed():
        db.close()  # Fechar a conexão após cada requisição

if __name__ == '__main__':
    inicializar_tabelas() 
    app.run(debug=True)
