from models.usuario import Usuario
from middlewares.exceptions import UsuarioOuSenhaIncorretos, CamposNaoPreenchidos
from peewee import DoesNotExist

class LoginController():
    def __init__(self, email, senha):
      if not email or not senha:
        raise CamposNaoPreenchidos('Todos os campos devem ser preenchidos')
      self.email = email
      self.senha = senha

    def validar_login(self):
      try:
        usuario = Usuario.get(Usuario.email == self.email)

        if usuario.senha != self.senha:
            raise UsuarioOuSenhaIncorretos("Usuário ou senha incorretos")

        return True
      except DoesNotExist:
        raise UsuarioOuSenhaIncorretos("Usuário ou senha incorretos")
