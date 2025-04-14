import re
from exceptions import *

class Usuario: 
    def __init__(self, nome, sobrenome, email, senha, confirmacao_senha):
        if not nome or not sobrenome or not email or not senha or not confirmacao_senha:
            raise CamposNaoPreenchidos('Todos os campos devem ser preenchidos')

        self.nome = nome        
        self.sobrenome = sobrenome
        self.email = str(email)
        self.senha = str(senha)
        self.confirmacao_senha = str(confirmacao_senha)

        # Começar as validações
        self.senha_valida = self.validar_senha()
        self.email_valido = self.validar_email()

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

        if not re.match(pattern, self.email):
            raise CadastroInvalido('E-mail inválido')
        return True
    
    def __bool__(self):
        return self.senha_valida and self.email_valido
    
