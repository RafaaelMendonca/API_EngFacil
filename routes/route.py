from flask import request, jsonify, session
from controllers.cadastro import UsuarioController
from controllers.login import LoginController
from controllers.projetos import ProjetosController
from middlewares.exceptions import CadastroInvalido, CamposNaoPreenchidos, UsuarioOuSenhaIncorretos, ProjetoJaCadastrado
from main import app
from models.usuario import Usuario
from models.banco import Projeto

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
      usuario = Usuario.get(Usuario.email == dados.get('email'))
      session['usuario_id'] = usuario.id
      return jsonify({'mensagem': 'Login realizado com sucesso!'}), 200
  except CamposNaoPreenchidos as e:
    return jsonify({"message": str(e)}), 400
  except UsuarioOuSenhaIncorretos as e:
    return jsonify({'mensagem': str(e)}), 401

@app.route('/logout')
def logout():
  session.clear()
  return jsonify({'mensagem': 'Usuario desconectado'})
# --------------- projetos -------------
# adicionar a função e a rota para dicionar os projetos (como que vou colocar os projetos no painel se eu nem cadastrei os projetos)
@app.route('/projetos', methods=['POST'])
def adicionar_projeto():
    usuario_id = session.get('usuario_id')

    if not usuario_id:
        return jsonify({'mensagem': 'Usuário não está logado'}), 401

    try:
        dados = request.json
        usuario = Usuario.get_by_id(usuario_id)

        controller = ProjetosController()
        controller.adicionar_projeto(
            nome_projeto=dados.get('nome_projeto'),
            custo_planejado=dados.get('custo_planejado'),
            custo_real=dados.get('custo_real'),
            duracao_planejada=dados.get('duracao_planejada'),
            duracao_real=dados.get('duracao_real'),
            horas_trabalhadas=dados.get('horas_trabalhadas'),
            indice_risco_seguranca=dados.get('indice_risco_seguranca'),
            anomalia_detectada=dados.get('anomalia_detectada'),
            desvio_cronograma=dados.get('desvio_cronograma'),
            umidade=dados.get('umidade'),
            utilizacao_equipamento=dados.get('utilizacao_equipamento'),
            vibracao=dados.get('vibracao'),
            largura_fissura=dados.get('largura_fissura'),
            usuario=usuario  # Aqui está o segredo!
        )

        return jsonify({'mensagem': 'Projeto cadastrado com sucesso!'}), 201

    except CamposNaoPreenchidos as e:
        return jsonify({'erro': str(e)}), 400
    except ProjetoJaCadastrado as e:
        return jsonify({'erro': str(e)}), 409
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Erro interno no servidor.'}), 500
# pensar em como eu transferiria para o modelo treinado



# --------------- painel ---------------

@app.route('/painel', methods=['GET'])
def painel():
    usuario_id = session.get('usuario_id')

    if not usuario_id:
        return jsonify({'mensagem': 'Usuário não está logado'}), 401

    try:
        usuario = Usuario.get_by_id(usuario_id)
        projetos = Projeto.select().where(Projeto.usuario == usuario)

        lista_projetos = []
        #adicionar o restante do banco, sao 13 se nao me engano
        # verificar para adicionar um controle para os projetos
        """
        for p in projetos:
            lista_projetos.append({
                'nome_projeto': p.nome_projeto,
                'custo_planejado': float(p.custo_planejado),
                'custo_real': float(p.custo_real),
                'duracao_planejada': p.duracao_planejada,
                'duracao_real': p.duracao_real,
                'horas_trabalhadas': p.horas_trabalhadas
            })
        """

        return jsonify(lista_projetos), 200

    except Usuario.DoesNotExist:
        return jsonify({'mensagem': 'Usuário inválido'}), 400
      #------------------------- remocao ------------------------

