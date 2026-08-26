"""Utilitário compartilhado pelos Repositories que chamam stored procedures."""
from datetime import datetime


def normalizar_linha(linha):
    """
    Converte uma linha (RowMapping) retornada por uma stored procedure
    em um dict simples e serializável em JSON (datetime -> isoformat).
    """
    dados = dict(linha)
    for campo, valor in dados.items():
        if isinstance(valor, datetime):
            dados[campo] = valor.isoformat()
    return dados
