from middlewares.exceptions import CamposNaoPreenchidos, ProjetoJaCadastrado
from models.banco import Projeto
from models.usuario import Usuario

class ProjetosController:
    def adicionar_projeto(self,
                 nome_projeto:str,
                 custo_planejado:float,
                 custo_real:float,
                 duracao_planejada:int,
                 duracao_real:int,
                 horas_trabalhadas:int,
                 indice_risco_seguranca:float,
                 anomalia_detectada:int,
                 desvio_cronograma:float,
                 umidade:float,
                 utilizacao_equipamento:float,
                 vibracao:float,
                 largura_fissura:float,
                 usuario: Usuario):
        
        campos = [nome_projeto, custo_planejado, custo_real, duracao_planejada, duracao_real,
          horas_trabalhadas, indice_risco_seguranca, anomalia_detectada, desvio_cronograma,
          umidade, utilizacao_equipamento, vibracao, largura_fissura]
        
        if any(campo is None for campo in campos):
            raise CamposNaoPreenchidos('Todos os campos devem ser preenchidos') 
        
        # validacao para ver se ja existe o projeto com o mesmo nome no banco de dados
        if Projeto.select().where(Projeto.nome_projeto == nome_projeto, Projeto.usuario == usuario).exists():
            raise ProjetoJaCadastrado('O projeto com este nome já está cadastrado.')

        Projeto.create(
            nome_projeto = nome_projeto,
            custo_planejado = custo_planejado,
            custo_real = custo_real,
            duracao_planejada = duracao_planejada,
            duracao_real = duracao_real,
            horas_trabalhadas = horas_trabalhadas,
            indice_risco_seguranca = indice_risco_seguranca,
            anomalia_detectada = anomalia_detectada,
            desvio_cronograma = desvio_cronograma,
            umidade = umidade,
            utilizacao_equipamento = utilizacao_equipamento,
            vibracao = vibracao,
            largura_fissura = largura_fissura,
            usuario = usuario       
        )
        return True