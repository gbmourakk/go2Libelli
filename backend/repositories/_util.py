                                                                               
from datetime import datetime


def normalizar_linha(linha):
       
                                                                      
                                                                      
       
    dados = dict(linha)
    for campo, valor in dados.items():
        if isinstance(valor, datetime):
            dados[campo] = valor.isoformat()
    return dados
