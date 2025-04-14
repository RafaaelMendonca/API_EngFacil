from main import app
from cadastro import Usuario
from flask import request, redirect, url_for, jsonify
from exceptions import CadastroInvalido, CamposNaoPreenchidos

@app.route('/')
def home():
    return "Bem-vindo à página inicial!"

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    try:
        if request.method == 'POST':
            dados = request.json
            nome = dados.get('nome')
            sobrenome = dados.get('sobrenome')
            email = dados.get('email')
            senha = dados.get('senha')
            confirmacao_senha = dados.get('confirmacao_senha')

            usuario = Usuario(nome, sobrenome, email, senha, confirmacao_senha)

            if usuario:
                return redirect(url_for('login'))

        return 'Área de cadastro'
    
    except CamposNaoPreenchidos as e:
        return jsonify({"error": str(e)}), 400
    except CadastroInvalido as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno no servidor."}), 500

@app.route('/login')
def login():
    return 'Essa é a pagina de login'

# Falta adicionar o banco de dados, não permitir que mais de um usuario se cadastre com o mesmo email