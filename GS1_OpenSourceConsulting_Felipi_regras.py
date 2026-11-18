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
ARQUIVO     : GS1_OpenSourceConsulting_Felipi_regras.py
VERSÃO      : 1.1 (modularizada com type hints)
DESCRIÇÃO   : Regras de negócio: classificação, ranking e simulação. Funções puras, sem
              entrada/saída no terminal, sem arquivos e sem estado compartilhado.
=====================================================================
"""

from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------
# CONSTANTES E CRITÉRIOS (tabela única do grupo)
# ---------------------------------------------------------------------

LUGARES_POR_MESA: int = 3

MESAS_SALA_GRANDE: int = 4  # a partir de 4 mesas a sala é "grande" (RN-02)

# Critérios de conforto: tabela única de limiares do grupo (proposta de
# 08/11/2026, aprovada pelo grupo). As comparações são ESTRITAS (< e >): o
# próprio limite fica do lado de dentro.
#   "faixa"   = (limite baixo, limite alto): usa o 1º rótulo se v < limite
#               baixo, o 3º se v > limite alto e o 2º nos demais casos. Só
#               indica ONDE o valor está, sem dizer se é bom ou ruim.
#   "rotulos" = nomes das três faixas, já com a concordância de cada grandeza.
#   "limites" = (crítico abaixo, atenção abaixo, atenção acima, crítico acima):
#               crítico se v < 1º ou v > 4º; senão atenção se v < 2º ou v > 3º;
#               senão adequado. None = esse lado não gera alerta.
#   "leitura" = leituras possíveis; fora desse intervalo a leitura é impossível.
CRITERIOS: Dict[str, Dict[str, Any]] = {
    "temperatura": {"rotulo": "Temperatura", "unidade": "°C",
                    "faixa": (21, 26), "limites": (18, 21, 25, 26),
                    "rotulos": ("baixa", "média", "alta"),
                    "leitura": (-40, 80)},
    "luz": {"rotulo": "Luminosidade", "unidade": "lux (estimado)",
            "faixa": (300, 750), "limites": (200, 300, 2000, 3000),
            "rotulos": ("baixa", "média", "alta"),
            "leitura": (0, 100000)},
    "ruido": {"rotulo": "Ruído", "unidade": "dB (simulado)",
              "faixa": (40, 55), "limites": (None, None, 45, 65),
              "rotulos": ("silencioso", "moderado", "barulhento"),
              "leitura": (30, 80)},
    "ocupacao": {"rotulo": "Ocupação", "unidade": "%",
                 "faixa": (35, 70), "limites": (None, None, 50, 90),
                 "rotulos": ("baixa", "média", "alta"),
                 "leitura": (0, 100)},
}

# Escala do ruído simulado: 30 dB = índice 0 e 80 dB = índice 100.
ESCALA_DB_INDICE: Tuple[float, float] = (30.0, 80.0)

# Pesos (somam 100) de cada critério por atividade, conforme a tabela do grupo.
# "vagas" = lugares vagos em relação à capacidade da sala; "mesas" = mesas
# totalmente livres (cada uma vale 1/4 do peso, até 4 mesas). Pontuação didática.
PESOS: Dict[str, Dict[str, int]] = {
    "sozinho": {"ruido": 40, "temperatura": 20, "luz": 20, "vagas": 20, "mesas": 0},
    "grupo": {"ruido": 20, "temperatura": 10, "luz": 10, "vagas": 25, "mesas": 35},
    "video": {"ruido": 35, "temperatura": 0, "luz": 10, "vagas": 20, "mesas": 35},
}

MESAS_PARA_PESO_INTEIRO: int = 4

# Folga mínima ao arredondar a pontuação: absorve o erro de ponto flutuante nos
# empates de meio ponto (ex.: 21,499999999999996 deve valer 21,5 e subir).
TOLERANCIA_ARREDONDAMENTO: float = 0.000000001

# Ruído máximo (dB simulados) para a sala poder ser indicada; None = sem limite.
LIMITE_RUIDO_ATIVIDADE: Dict[str, Optional[int]] = {"sozinho": None, "grupo": 65, "video": 45}

# No vídeo o silêncio pontua mais: o peso inteiro até 30 dB, caindo em linha
# reta até zero em 45 dB simulados.
RUIDO_VIDEO: Tuple[float, float] = (30.0, 45.0)

# Fração dos pontos de um critério conforme sua classificação.
PONTOS_CLASSE: Dict[str, float] = {"adequado": 1.0, "atenção": 0.5, "crítico": 0.0}

# Equivalência com os LEDs da sala-modelo (disciplina de Edge).
SEMAFORO: Dict[str, str] = {"adequado": "verde", "atenção": "amarelo", "crítico": "vermelho"}


# ---------------------------------------------------------------------
# REGRAS DE NEGÓCIO
# ---------------------------------------------------------------------


def capacidade(sala: Dict[str, Any]) -> int:
    """Capacidade sentada da sala (3 lugares por mesa)."""
    return len(sala["mesas"]) * LUGARES_POR_MESA


def ocupacao_total(sala: Dict[str, Any]) -> int:
    """Soma das pessoas sentadas em todas as mesas."""
    return sum(sala["mesas"])


def vagas_individuais(sala: Dict[str, Any]) -> int:
    """Quantidade de lugares vagos na sala."""
    return capacidade(sala) - ocupacao_total(sala)


def mesas_vazias(sala: Dict[str, Any]) -> int:
    """Quantidade de mesas totalmente livres."""
    quantidade: int = 0
    for pessoas in sala["mesas"]:
        if pessoas == 0:
            quantidade += 1
    return quantidade


def taxa_ocupacao(sala: Dict[str, Any]) -> float:
    """Taxa de ocupação da sala, em porcentagem."""
    return 100.0 * ocupacao_total(sala) / capacidade(sala)


def tipo_sala(quantidade_mesas: int) -> str:
    """Classifica o porte da sala pelo número de mesas."""
    if quantidade_mesas <= 2:
        return "pequena"
    elif quantidade_mesas == 3:
        return "média"
    else:
        return "grande"


def passou_dos_limites(valor: float, limite_abaixo: Optional[float], limite_acima: Optional[float]) -> bool:
    """True se valor < limite_abaixo ou valor > limite_acima (None = ignora)."""
    if limite_abaixo is not None and valor < limite_abaixo:
        return True
    if limite_acima is not None and valor > limite_acima:
        return True
    return False


def classificar_valor(valor: float, limites: Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]) -> str:
    """Severidade: 'adequado', 'atenção' ou 'crítico' (limites estritos).

    limites = (crítico abaixo, atenção abaixo, atenção acima, crítico acima).
    """
    critico_abaixo, atencao_abaixo, atencao_acima, critico_acima = limites
    if passou_dos_limites(valor, critico_abaixo, critico_acima):
        return "crítico"
    elif passou_dos_limites(valor, atencao_abaixo, atencao_acima):
        return "atenção"
    else:
        return "adequado"


def valores_da_sala(sala: Dict[str, Any]) -> Dict[str, float]:
    """Retorna os quatro valores avaliados da sala em um dicionário."""
    return {"temperatura": float(sala["temperatura"]), "luz": float(sala["luz"]),
            "ruido": float(sala["ruido"]), "ocupacao": taxa_ocupacao(sala)}


def classificar_sala(sala: Dict[str, Any]) -> Dict[str, str]:
    """Retorna a classificação de cada critério da sala."""
    valores = valores_da_sala(sala)
    classes: Dict[str, str] = {}
    for chave in CRITERIOS:
        classes[chave] = classificar_valor(valores[chave],
                                           CRITERIOS[chave]["limites"])
    return classes


def estado_geral(classes: Dict[str, str]) -> str:
    """Estado geral: crítico se algum crítico; atenção se algum atenção."""
    lista = list(classes.values())
    if "crítico" in lista:
        return "crítico"
    elif "atenção" in lista:
        return "atenção"
    else:
        return "adequado"


def classificar_faixa(valor: float, chave: str) -> str:
    """Retorna o rótulo da faixa (ex.: baixa/média/alta), sem julgar conforto."""
    limite_baixo, limite_alto = CRITERIOS[chave]["faixa"]
    rotulos = CRITERIOS[chave]["rotulos"]
    if valor < limite_baixo:
        return rotulos[0]
    elif valor > limite_alto:
        return rotulos[2]
    else:
        return rotulos[1]


def calcular_indice_ruido(db_simulado: float) -> int:
    """Converte dB simulados em índice de ruído: 0 (silêncio) a 100.

    O meio arredonda para cima (0,5 vira 1), igual ao ESP32 e ao site.
    O valor já está entre 0 e 100 ao arredondar, então int() equivale a floor.
    """
    db_min, db_max = ESCALA_DB_INDICE
    indice: float = 100.0 * (db_simulado - db_min) / (db_max - db_min)
    indice = max(0.0, min(100.0, indice))
    return int(indice + 0.5)


def rotulo_mesa(pessoas: int) -> str:
    """Rótulo de uso de uma mesa conforme as pessoas sentadas."""
    if pessoas == 0:
        return "LIVRE PARA GRUPO"
    elif pessoas == LUGARES_POR_MESA:
        return "LOTADA"
    else:
        return "parcial"


def resumo_consolidado(salas: List[Dict[str, Any]]) -> Tuple[int, int, int, int, Dict[str, int]]:
    """Retorna (ocupados, lugares, mesas vazias, mesas, contagem de estados)."""
    ocupados: int = 0
    lugares: int = 0
    vazias: int = 0
    mesas: int = 0
    contagem: Dict[str, int] = {"adequado": 0, "atenção": 0, "crítico": 0}
    for sala in salas:
        ocupados += ocupacao_total(sala)
        lugares += capacidade(sala)
        vazias += mesas_vazias(sala)
        mesas += len(sala["mesas"])
        contagem[estado_geral(classificar_sala(sala))] += 1
    return ocupados, lugares, vazias, mesas, contagem


def buscar_sala(salas: List[Dict[str, Any]], texto: str) -> Optional[Dict[str, Any]]:
    """Busca pelo número da lista (ex.: 3) ou pelo ID (ex.: S03)."""
    texto = texto.strip().upper()
    numero: Optional[int]
    try:
        numero = int(texto)
    except ValueError:
        numero = None
    if numero is not None:
        if 1 <= numero <= len(salas):
            return salas[numero - 1]
        return None
    for sala in salas:
        if sala["id"].upper() == texto:
            return sala
    return None


def respeita_regra_sala_grande(mesas: List[int]) -> bool:
    """RN-02: a sala grande (4 mesas ou mais) mantém uma mesa totalmente livre."""
    if len(mesas) >= MESAS_SALA_GRANDE:
        return 0 in mesas
    return True


def motivo_inelegivel(sala: Dict[str, Any], atividade: str) -> str:
    """Retorna o motivo de a sala não servir à atividade ('' se servir).

    A primeira regra que falhar é a mostrada: sala lotada, falta de mesa
    totalmente livre (grupo e vídeo) e ruído acima do limite da atividade.
    """
    limite_ruido = LIMITE_RUIDO_ATIVIDADE[atividade]
    if atividade in ("sozinho", "video") and vagas_individuais(sala) == 0:
        return "sala lotada"
    if atividade in ("grupo", "video") and mesas_vazias(sala) == 0:
        return "nenhuma mesa totalmente livre"
    if limite_ruido is not None and sala["ruido"] > limite_ruido:
        return f"ruído acima de {limite_ruido} dB simulados"
    return ""


def pontos_silencio_video(db_simulado: float, peso: float) -> float:
    """Vídeo: peso inteiro até 30 dB, caindo linearmente a zero em 45 dB."""
    db_min, db_max = RUIDO_VIDEO
    fracao: float = (db_max - db_simulado) / (db_max - db_min)
    return peso * max(0.0, min(1.0, fracao))


def pontuar_sala(sala: Dict[str, Any], atividade: str) -> int:
    """Pontuação de 0 a 100 da sala para a atividade (determinística).

    Ruído, temperatura e luz: peso inteiro se adequado, metade se atenção e
    zero se crítico (no vídeo o ruído pontua pelo silêncio, em linha reta).
    Vagas: proporcional à capacidade. Mesas livres: 1/4 do peso por mesa.
    O meio ponto arredonda para cima (21,5 vira 22), como no site.
    """
    pesos = PESOS[atividade]
    classes = classificar_sala(sala)
    total: float
    if atividade == "video":
        total = pontos_silencio_video(float(sala["ruido"]), float(pesos["ruido"]))
    else:
        total = float(pesos["ruido"]) * PONTOS_CLASSE[classes["ruido"]]
    total += float(pesos["temperatura"]) * PONTOS_CLASSE[classes["temperatura"]]
    total += float(pesos["luz"]) * PONTOS_CLASSE[classes["luz"]]
    total += float(pesos["vagas"]) * vagas_individuais(sala) / capacidade(sala)
    livres: int = min(mesas_vazias(sala), MESAS_PARA_PESO_INTEIRO)
    total += float(pesos["mesas"]) * livres / MESAS_PARA_PESO_INTEIRO
    return int(total + 0.5 + TOLERANCIA_ARREDONDAMENTO)


def vem_antes(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    """True se o item a deve aparecer antes do item b no ranking (RN-15).

    Ordem: mais pontos; no empate, menor taxa de ocupação; depois, mais
    mesas totalmente livres; por fim, o ID em ordem alfabética.
    """
    if a["pontos"] != b["pontos"]:
        return a["pontos"] > b["pontos"]
    if a["taxa"] != b["taxa"]:
        return a["taxa"] < b["taxa"]
    if a["livres"] != b["livres"]:
        return a["livres"] > b["livres"]
    return a["sala"]["id"].upper() < b["sala"]["id"].upper()


def ordenar_ranking(ranking: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ordena a lista de itens do melhor para o pior (insertion sort)."""
    for i in range(1, len(ranking)):
        atual = ranking[i]
        j = i - 1
        while j >= 0 and vem_antes(atual, ranking[j]):
            ranking[j + 1] = ranking[j]
            j -= 1
        ranking[j + 1] = atual
    return ranking


def montar_ranking(salas: List[Dict[str, Any]], atividade: str) -> Tuple[List[Dict[str, Any]], List[Tuple[Dict[str, Any], str]]]:
    """Retorna (itens do ranking ordenados, lista de (sala, motivo) excluídas).

    Cada item é um dicionário com: pontos, taxa, livres e sala.
    """
    ranking: List[Dict[str, Any]] = []
    excluidas: List[Tuple[Dict[str, Any], str]] = []
    for sala in salas:
        motivo: str = motivo_inelegivel(sala, atividade)
        if motivo == "":
            ranking.append({"pontos": pontuar_sala(sala, atividade),
                            "taxa": taxa_ocupacao(sala),
                            "livres": mesas_vazias(sala), "sala": sala})
        else:
            excluidas.append((sala, motivo))
    return ordenar_ranking(ranking), excluidas


def dentro_da_faixa(valor: float, faixa: Tuple[Optional[float], Optional[float]]) -> bool:
    """Verifica se valor está na faixa (mínimo, máximo); None ignora."""
    minimo, maximo = faixa
    if minimo is not None and valor < minimo:
        return False
    if maximo is not None and valor > maximo:
        return False
    return True


def valor_do_filtro(sala: Dict[str, Any], chave: str) -> float:
    """Retorna o valor da sala correspondente à chave do filtro."""
    if chave == "ocupacao":
        return float(ocupacao_total(sala))
    elif chave == "mesas_vazias":
        return float(mesas_vazias(sala))
    else:
        return float(sala[chave])


def filtrar_salas(salas: List[Dict[str, Any]], filtros: Dict[str, Tuple[Optional[float], Optional[float]]]) -> List[Dict[str, Any]]:
    """Retorna as salas que atendem a todos os filtros ativos."""
    resultado: List[Dict[str, Any]] = []
    for sala in salas:
        atende: bool = True
        for chave in filtros:
            if not dentro_da_faixa(valor_do_filtro(sala, chave), filtros[chave]):
                atende = False
                break
        if atende:
            resultado.append(sala)
    return resultado


def alterar_mesa(sala: Dict[str, Any], indice: int, variacao: int) -> Tuple[bool, str]:
    """Aplica +1/-1 em uma mesa. Retorna (sucesso, mensagem)."""
    atual: int = sala["mesas"][indice]
    novo: int = atual + variacao
    if novo > LUGARES_POR_MESA:
        return False, "Operação recusada: a mesa já está cheia (3/3)."
    elif novo < 0:
        return False, "Operação recusada: a mesa já está vazia (0/3)."
    mesas_novas = list(sala["mesas"])
    mesas_novas[indice] = novo
    if not respeita_regra_sala_grande(mesas_novas):
        maximo: int = (len(mesas_novas) - 1) * LUGARES_POR_MESA
        return False, ("Operação recusada: em sala grande a simulação mantém "
                       f"uma mesa totalmente livre (até {maximo} pessoas).")
    sala["mesas"][indice] = novo
    return True, f"Mesa {indice + 1} agora com {novo}/{LUGARES_POR_MESA} pessoas."