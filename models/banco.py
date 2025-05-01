from peewee import *
from usuario import Usuario
db = SqliteDatabase('cadastro.db')

class Projeto(Model):
     nome_projeto = TextField(unique=True)
     custo_planejado = DecimalField(decimal_places=2, max_digits=12) # com maximo de digitos 12, chegaremos até a casa do bilhao
     custo_real = DecimalField(decimal_places=2, max_digits=12)
     duracao_planejada = IntegerField()
     duracao_real = IntegerField()
     horas_trabalhadas = IntegerField()
     indice_risco_seguranca = DecimalField(max_digits=4,decimal_places=2)
     anomalia_detectada = IntegerField()
     desvio_cronograma = DecimalField(max_digits=7, decimal_places=2)
     umidade = DecimalField(max_digits=4, decimal_places=2)
     utilizacao_equipamento = DecimalField(max_digits=4, decimal_places=2)
     vibracao = DecimalField(max_digits=4, decimal_places=2)
     largura_fissura = DecimalField(max_digits=4, decimal_places=2)

     usuario = ForeignKeyField(Usuario, backref='projetos')


     class Meta:
         database = db

