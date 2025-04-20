from flask import request, jsonify
from controllers.cadastro import UsuarioController
from controllers.login import LoginController
from middlewares.exceptions import CadastroInvalido, CamposNaoPreenchidos, UsuarioOuSenhaIncorretos
from main import app
from models.usuario import Usuario

@app.route('/')
def listar_usuarios():
    usuarios = Usuario.select()
    dados = []
    for u in usuarios:
        dados.append({
            'id': u.id,
            'nome': u.nome,
            'email': u.email
            # a senha está sendo omitida de propósito
        })
    return jsonify(dados)

@app.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        dados = request.json
        print(f"Dados recebidos: {dados}")
        usuario = UsuarioController(
            dados.get('nome'),
            dados.get('email'),
            dados.get('senha'),
            dados.get('confirmacao_senha')
        )
        if usuario.validar_cadastro():
            usuario.cadastrar_usuario()
            print('Cadastrado no banco de dados com sucesso!')
            return jsonify({"message": "Cadastro realizado com sucesso!"}), 201
        
    except CamposNaoPreenchidos as e:
        return jsonify({"error": str(e)}), 400
    except CadastroInvalido as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"error": "Erro interno no servidor."}), 500

@app.route('/login', methods=['POST'])
def login():
  try:
    dados = request.json
    login_usuario = LoginController(
        dados.get('email'),
        dados.get('senha')
        )
    if login_usuario.validar_login():
      return jsonify({'mensagem': 'Login realizado com sucesso!'}), 200
  except CamposNaoPreenchidos as e:
    return jsonify({"message": str(e)}), 400
  except UsuarioOuSenhaIncorretos as e:
    return jsonify({'mensagem': str(e)}), 401

@app.route('/painel', methods=['GET'])
def painel():
    return jsonify({"projetos": "sucesso"}), 200
