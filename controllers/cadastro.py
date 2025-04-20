import re
from middlewares.exceptions import *
from models.usuario import Usuario

class UsuarioController: 
    def __init__(self, nome, email, senha, confirmacao_senha):
        if not nome or not email or not senha or not confirmacao_senha:
            raise CamposNaoPreenchidos('Todos os campos devem ser preenchidos')

        self.nome = nome
        self.email = str(email)
        self.senha = str(senha)
        self.confirmacao_senha = str(confirmacao_senha)

        # Começar as validações
        

    def validar_cadastro(self):
        if self.validar_senha() and self.validar_email():
            
            return True

    def validar_senha(self):
        if self.confirmacao_senha != self.senha:
            raise CadastroInvalido('Senhas diferentes')
        
        senha_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+<>?]).{8,}$'
        if not re.match(senha_regex, self.senha):
            raise CadastroInvalido('A senha deve conter ao menos 8 caracteres, incluir uma letra maiúscula, um numero e um caractere especial')
        
        return True

    def validar_email(self):
        pattern = (r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
                   r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
        
        if Usuario.select().where(Usuario.email == self.email).exists():
            raise CadastroInvalido("Este e-mail já está cadastrado!")

        if not re.match(pattern, self.email):
            raise CadastroInvalido('E-mail inválido')
        return True
    
    def cadastrar_usuario(self):
        # linkar com o banco para os devidos cadastros, lembrando que o confirmacao_senha é apenas para confirmar na hora do cadastro
        # provavelmente nao colocarei o cadastro no banco aqui
        Usuario.create(
                nome=self.nome,
                email=self.email,
                senha=self.senha
                )
        print(f'Usuário {self.nome}cadastrado com sucesso!')
        return True

    
    def __bool__(self):
        return self.senha_valida and self.email_valido

