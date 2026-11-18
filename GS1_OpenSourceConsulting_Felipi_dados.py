"""
=====================================================================
PROJETO     : Study Comfort
EQUIPE      : Open Source Consulting
INTEGRANTES :
    Daniel Roberto           - RM 571746
    Felipe Pedrol            - RM 569631
    Jecky Cossio             - RM 572226
    Felipi Bandeira de Godoy - RM 573741
DISCIPLINA  : Computational Thinking with Python
ARQUIVO     : GS1_OpenSourceConsulting_Felipi_dados.py
VERSÃO      : 1.1 (modularizada com type hints)
DESCRIÇÃO   : Dados: salas de demonstração, estado do programa e arquivo JSON
              (salvar, carregar e validar). Não imprime nada na tela.
=====================================================================
"""

import json
import os
from typing import Any, Dict, List, Optional, Tuple
from GS1_OpenSourceConsulting_Felipi_regras import (
    CRITERIOS, LUGARES_POR_MESA, respeita_regra_sala_grande,
)


# ---------------------------------------------------------------------
# CONSTANTES E ESTADO
# ---------------------------------------------------------------------

ARQUIVO_DADOS: str = "dados_study_comfort.json"

# Estado do programa (dicionário mutável compartilhado pelas funções).
ESTADO: Dict[str, Any] = {"salas": [], "alterado": False}


# ---------------------------------------------------------------------
# DADOS: DEMONSTRAÇÃO, JSON E VALIDAÇÃO
# ---------------------------------------------------------------------


def criar_salas_demo() -> List[Dict[str, Any]]:
    """Retorna a lista de salas de demonstração (dados fictícios)."""
    modelo: str = "Exemplo do contrato (simulação em Python)"
    demo: str = "Dados demonstrativos"
    return [
        {"id": "S01", "nome": "Sala de Estudo 01", "mesas": [1, 2, 0],
         "temperatura": 22.8, "luz": 410, "ruido": 54, "fonte": modelo},
        {"id": "S02", "nome": "Sala de Estudo 02", "mesas": [0, 2],
         "temperatura": 22.0, "luz": 410, "ruido": 42, "fonte": demo},
        {"id": "S03", "nome": "Sala de Estudo 03", "mesas": [3, 3],
         "temperatura": 18.0, "luz": 920, "ruido": 71, "fonte": demo},
        {"id": "S04", "nome": "Sala de Estudo 04", "mesas": [1, 1, 1],
         "temperatura": 21.0, "luz": 500, "ruido": 46, "fonte": demo},
        {"id": "S05", "nome": "Sala de Estudo 05", "mesas": [0, 3, 3],
         "temperatura": 24.0, "luz": 350, "ruido": 57, "fonte": demo},
        {"id": "S06", "nome": "Sala de Estudo 06", "mesas": [2, 2, 1],
         "temperatura": 19.0, "luz": 180, "ruido": 61, "fonte": demo},
        {"id": "S07", "nome": "Sala de Estudo 07", "mesas": [0, 0, 1],
         "temperatura": 23.0, "luz": 450, "ruido": 39, "fonte": demo},
        {"id": "S08", "nome": "Sala de Estudo 08", "mesas": [3, 2, 1, 0],
         "temperatura": 25.0, "luz": 600, "ruido": 53, "fonte": demo},
        {"id": "S09", "nome": "Sala de Estudo 09", "mesas": [3, 3, 3, 0],
         "temperatura": 28.0, "luz": 760, "ruido": 68, "fonte": demo},
    ]


def caminho_arquivo() -> str:
    """Retorna o caminho do JSON, na mesma pasta deste script."""
    pasta: str = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pasta, ARQUIVO_DADOS)


def eh_numero(valor: Any) -> bool:
    """Retorna True se valor for int ou float (excluindo bool)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def validar_sala(sala: Dict[str, Any], ids_vistos: List[str]) -> Tuple[bool, str]:
    """Valida uma sala lida do JSON. Retorna (ok, mensagem)."""
    campos: Tuple[str, ...] = ("id", "nome", "mesas", "temperatura", "luz", "ruido", "fonte")
    if not isinstance(sala, dict):
        return False, "Há uma sala com formato inválido."
    for campo in campos:
        if campo not in sala:
            return False, f"Sala sem o campo '{campo}'."
    if not isinstance(sala["id"], str):
        return False, "Identificador de sala inválido."
    identificador: str = sala["id"].strip().upper()
    if identificador == "" or identificador != sala["id"].upper():
        return False, "Identificador de sala vazio ou com espaços nas pontas."
    if identificador in ids_vistos:
        return False, (f"Identificador repetido: {sala['id']} "
                       "(maiúsculas e minúsculas contam como iguais).")
    if not isinstance(sala["nome"], str) or not isinstance(sala["fonte"], str):
        return False, f"Sala {sala['id']}: nome/fonte inválidos."
    mesas = sala["mesas"]
    if not isinstance(mesas, list) or len(mesas) < 1 or len(mesas) > 10:
        return False, f"Sala {sala['id']}: lista de mesas inválida."
    for pessoas in mesas:
        if not isinstance(pessoas, int) or isinstance(pessoas, bool) \
                or pessoas < 0 or pessoas > LUGARES_POR_MESA:
            return False, f"Sala {sala['id']}: ocupação de mesa inválida."
    if not respeita_regra_sala_grande(mesas):
        return False, (f"Sala {sala['id']}: sala grande deve manter ao menos "
                       "uma mesa totalmente livre.")
    for chave in ("temperatura", "luz", "ruido"):
        minimo, maximo = CRITERIOS[chave]["leitura"]
        valor = sala[chave]
        if not eh_numero(valor) or not (minimo <= valor <= maximo):
            return False, f"Sala {sala['id']}: valor de '{chave}' inválido."
    return True, "Sala válida."


def validar_dados(dados: Dict[str, Any]) -> Tuple[bool, str]:
    """Valida o conteúdo carregado do JSON. Retorna (ok, mensagem)."""
    if not isinstance(dados, dict) or "salas" not in dados:
        return False, "Estrutura inválida: chave 'salas' ausente."
    salas = dados["salas"]
    if not isinstance(salas, list) or len(salas) == 0:
        return False, "A lista de salas está vazia ou inválida."
    ids_vistos: List[str] = []
    for sala in salas:
        ok, mensagem = validar_sala(sala, ids_vistos)
        if not ok:
            return False, mensagem
        ids_vistos.append(sala["id"].strip().upper())
    return True, "Dados válidos."


def salvar_json(salas: List[Dict[str, Any]]) -> bool:
    """Grava as salas no arquivo JSON. Retorna True se deu certo."""
    dados: Dict[str, Any] = {"schema_version": 1, "salas": salas}
    try:
        with open(caminho_arquivo(), "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        return True
    except OSError:
        return False


def carregar_json() -> Tuple[Optional[List[Dict[str, Any]]], str]:
    """Lê o JSON. Retorna (salas, mensagem); salas é None em caso de erro."""
    try:
        with open(caminho_arquivo(), "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        return None, "Arquivo de dados não encontrado."
    except ValueError:
        return None, "Arquivo de dados corrompido ou ilegível."
    except OSError:
        return None, "Não foi possível abrir o arquivo de dados."
    ok, mensagem = validar_dados(dados)
    if not ok:
        return None, mensagem
    return dados["salas"], "Dados carregados com sucesso."