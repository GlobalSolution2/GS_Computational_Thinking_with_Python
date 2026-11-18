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
ARQUIVO     : GS1_OpenSourceConsulting_Felipi_interface.py
VERSÃO      : 1.1 (modularizada com type hints)
DESCRIÇÃO   : Interface com o usuário: telas, entrada de dados validada, saída do
              programa e funcionalidades do menu.
=====================================================================
"""

import os
from typing import Any, Dict, List, Optional, Tuple
from GS1_OpenSourceConsulting_Felipi_dados import (
    ESTADO, caminho_arquivo, carregar_json, criar_salas_demo, salvar_json,
)
from GS1_OpenSourceConsulting_Felipi_regras import (
    CRITERIOS, LIMITE_RUIDO_ATIVIDADE, LUGARES_POR_MESA, SEMAFORO,
    alterar_mesa, buscar_sala, calcular_indice_ruido, capacidade,
    classificar_faixa, classificar_sala, classificar_valor, estado_geral,
    filtrar_salas, mesas_vazias, montar_ranking, ocupacao_total,
    resumo_consolidado, rotulo_mesa, tipo_sala, vagas_individuais,
    valores_da_sala,
)


# ---------------------------------------------------------------------
# CONSTANTES DA INTERFACE
# ---------------------------------------------------------------------

VERSAO: str = "1.1"

LARGURA: int = 86

# Cada atividade: chave -> (identificador, nome exibido)
ATIVIDADES: Dict[int, Tuple[str, str]] = {
    1: ("sozinho", "Estudar sozinho"),
    2: ("grupo", "Trabalho em grupo"),
    3: ("video", "Gravar vídeo"),
}

# Filtros manuais: chave -> (rótulo, unidade, mínimo possível, máximo possível)
FILTROS_INFO: Dict[str, Tuple[str, str, float, float]] = {
    "ocupacao": ("Ocupação total", "pessoas", 0, 30),
    "mesas_vazias": ("Mesas totalmente livres", "mesas", 0, 10),
    "temperatura": ("Temperatura", "°C", -40, 80),
    "luz": ("Luminosidade", "lux", 0, 100000),
    "ruido": ("Ruído", "dB simulados", 30, 80),
}

OPCOES_FILTRO: Dict[int, str] = {1: "ocupacao", 2: "mesas_vazias", 3: "temperatura",
                 4: "luz", 5: "ruido"}


# ---------------------------------------------------------------------
# UTILITÁRIOS DE TELA
# ---------------------------------------------------------------------


def limpar_tela() -> None:
    """Limpa o terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def exibir_cabecalho(subtitulo: str) -> None:
    """Limpa a tela e exibe o cabeçalho padrão com o nome da tela atual."""
    limpar_tela()
    print("=" * LARGURA)
    print(f"  STUDY COMFORT | Monitoramento de Salas de Estudo (v{VERSAO})")
    print(f"  Tela: {subtitulo.capitalize()}")
    print("  Dica: digite SAIR a qualquer momento para encerrar o programa.")
    print("=" * LARGURA)


def pausar() -> None:
    """Aguarda o usuário pressionar ENTER."""
    ler_texto("\nPressione ENTER para continuar...")


# ---------------------------------------------------------------------
# ENTRADA DE DADOS (com validação e comando global SAIR)
# ---------------------------------------------------------------------


def perguntar_sim_nao(mensagem: str) -> bool:
    """Pergunta S/N e retorna True (sim) ou False (não)."""
    while True:
        resposta: str = input(mensagem).strip().upper()
        match resposta:
            case "S" | "SIM":
                return True
            case "N" | "NAO" | "NÃO":
                return False
            case _:
                print("Resposta inválida. Digite apenas S ou N.")


def ler_texto(mensagem: str) -> str:
    """Lê um texto. Se o usuário digitar SAIR, pede confirmação para sair."""
    while True:
        texto: str = input(mensagem).strip()
        if texto.upper() == "SAIR":
            solicitar_saida()
            continue
        return texto


def ler_inteiro(mensagem: str, minimo: int, maximo: int) -> int:
    """Lê um inteiro entre minimo e maximo (inclusive)."""
    while True:
        texto: str = ler_texto(mensagem)
        try:
            valor: int = int(texto)
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            continue
        if valor < minimo or valor > maximo:
            print(f"Valor fora do intervalo. Digite de {minimo} a {maximo}.")
        else:
            return valor


def ler_decimal(mensagem: str, minimo: float, maximo: float) -> float:
    """Lê um número decimal (aceita vírgula) entre minimo e maximo."""
    while True:
        texto: str = ler_texto(mensagem).replace(",", ".")
        try:
            valor: float = float(texto)
        except ValueError:
            print("Entrada inválida. Digite um número (ex.: 22,5).")
            continue
        if not (minimo <= valor <= maximo):
            print(f"Valor fora do intervalo. Digite de {minimo} a {maximo}.")
        else:
            return valor


def ler_decimal_opcional(mensagem: str, minimo: float, maximo: float) -> Optional[float]:
    """Como ler_decimal, mas ENTER vazio retorna None (ignorar)."""
    while True:
        texto: str = ler_texto(mensagem).replace(",", ".")
        if texto == "":
            return None
        try:
            valor: float = float(texto)
        except ValueError:
            print("Entrada inválida. Digite um número ou ENTER para ignorar.")
            continue
        if not (minimo <= valor <= maximo):
            print(f"Valor fora do intervalo. Digite de {minimo} a {maximo}.")
        else:
            return valor


# ---------------------------------------------------------------------
# SAÍDA DO PROGRAMA
# ---------------------------------------------------------------------


def solicitar_saida() -> None:
    """Pede confirmação (S/N) e encerra o programa se o usuário confirmar."""
    if perguntar_sim_nao("Deseja realmente sair? (S/N): "):
        encerrar_programa()
    else:
        print("Ok, continuando...")


def encerrar_programa() -> None:
    """Oferece salvar alterações pendentes e encerra o programa."""
    if ESTADO["alterado"]:
        pergunta: str = "Há alterações não salvas. Salvar antes de sair? (S/N): "
        if perguntar_sim_nao(pergunta):
            salvar_estado()
    print("\nObrigado por usar o Study Comfort. Até a próxima!")
    exit()


# ---------------------------------------------------------------------
# PERSISTÊNCIA (mensagens ao usuário)
# ---------------------------------------------------------------------


def salvar_estado() -> None:
    """Salva o estado atual e informa o resultado ao usuário."""
    if salvar_json(ESTADO["salas"]):
        ESTADO["alterado"] = False
        print(f"Dados salvos em: {caminho_arquivo()}")
    else:
        print("Erro: não foi possível salvar o arquivo.")


def inicializar_dados() -> None:
    """Carrega o JSON na abertura; cria o arquivo se ele não existir."""
    salas, mensagem = carregar_json()
    if salas is not None:
        ESTADO["salas"] = salas
        print("Dados anteriores carregados do arquivo JSON.")
    elif mensagem == "Arquivo de dados não encontrado.":
        ESTADO["salas"] = criar_salas_demo()
        salvar_estado()
        print("Primeiro uso: arquivo criado com dados de demonstração.")
    else:
        ESTADO["salas"] = criar_salas_demo()
        ESTADO["alterado"] = True
        print(f"Aviso: {mensagem}")
        print("Foram usados os dados de demonstração. O arquivo só será")
        print("substituído se você salvar.")


# ---------------------------------------------------------------------
# EXIBIÇÃO
# ---------------------------------------------------------------------


def descrever_criterios(sala: Dict[str, Any], atividade: str) -> str:
    """Resume os dados que mais pesam na recomendação da sala."""
    vagas: str = f"{vagas_individuais(sala)} lugar(es) vago(s)"
    livres: str = f"{mesas_vazias(sala)} mesa(s) livre(s)"
    faixa_ruido: str = classificar_faixa(sala["ruido"], "ruido")
    ruido: str = f"ruído {sala['ruido']:g} dB (faixa: {faixa_ruido})"
    match atividade:
        case "grupo":
            return f"{livres} | {vagas} | {ruido}"
        case "video":
            return f"{ruido} | {livres} | {vagas}"
        case _:
            return f"{vagas} | {ruido} | {sala['temperatura']:g} °C"


def descrever_regra(atividade: str) -> str:
    """Texto com a exigência da atividade para a sala ser indicada."""
    limite = LIMITE_RUIDO_ATIVIDADE[atividade]
    match atividade:
        case "grupo" | "video":
            return (f"Exige uma mesa totalmente livre e ruído de até {limite} "
                    "dB simulados.")
        case _:
            return "Exige ao menos um lugar vago."


def cabecalho_tabela() -> str:
    """Texto do cabeçalho comum das tabelas de salas."""
    return (f"{'ID':<5}{'Sala':<19}{'Porte':<9}{'Ocup.':<8}{'Livres':<8}"
            f"{'Temp.':<9}{'Luz':<10}{'Ruído':<9}Estado")


def formatar_linha(sala: Dict[str, Any]) -> str:
    """Formata uma sala em uma linha de tabela."""
    estado: str = estado_geral(classificar_sala(sala)).upper()
    ocupacao: str = f"{ocupacao_total(sala)}/{capacidade(sala)}"
    return (f"{sala['id']:<5}{sala['nome']:<19}"
            f"{tipo_sala(len(sala['mesas'])):<9}{ocupacao:<8}"
            f"{mesas_vazias(sala):<8}{sala['temperatura']:<9.1f}"
            f"{sala['luz']:<10.0f}{sala['ruido']:<9.0f}{estado}")


def exibir_tabela(salas: List[Dict[str, Any]], numerar: bool = True) -> None:
    """Exibe a tabela de salas (com coluna Nº opcional)."""
    prefixo: str = f"{'Nº':<4}" if numerar else ""
    print(prefixo + cabecalho_tabela())
    print("-" * LARGURA)
    for posicao, sala in enumerate(salas, start=1):
        numero: str = f"{posicao:<4}" if numerar else ""
        print(numero + formatar_linha(sala))


def exibir_resumo(salas: List[Dict[str, Any]]) -> None:
    """Exibe o resumo consolidado de todas as salas."""
    ocupados, lugares, vazias, mesas, contagem = resumo_consolidado(salas)
    print("-" * LARGURA)
    print(f"RESUMO ({len(salas)} salas): {ocupados}/{lugares} lugares ocupados"
          f" | {vazias}/{mesas} mesas totalmente livres")
    print(f"Semáforo: verde {contagem['adequado']} | "
          f"amarelo {contagem['atenção']} | vermelho {contagem['crítico']}")


def exibir_legenda() -> None:
    """Legenda das colunas da tabela."""
    print("\nOcup. = sentados/lugares | Livres = mesas totalmente livres")
    print("Temp. em °C | Luz em lux estimado | Ruído em dB simulado")
    print("Todos os valores são simulados ou fictícios.")


def exibir_detalhe(sala: Dict[str, Any]) -> None:
    """Exibe todas as informações de uma sala."""
    classes = classificar_sala(sala)
    valores = valores_da_sala(sala)
    geral: str = estado_geral(classes)
    quantidade: int = len(sala["mesas"])
    print(f"{sala['id']} - {sala['nome']} (sala {tipo_sala(quantidade)})")
    print(f"Origem dos dados: {sala['fonte']}")
    print(f"Capacidade: {capacidade(sala)} lugares em {quantidade} mesas")
    print(f"Ocupação: {ocupacao_total(sala)}/{capacidade(sala)} "
          f"({valores['ocupacao']:.0f}%) | faixa: "
          f"{classificar_faixa(valores['ocupacao'], 'ocupacao')} | "
          f"conforto: {classes['ocupacao'].upper()}")
    print(f"Lugares livres: {vagas_individuais(sala)} | "
          f"Mesas totalmente vazias: {mesas_vazias(sala)}")
    exibir_mesas(sala)
    print("\nCondições ambientais (simuladas):")
    for chave in ("temperatura", "luz", "ruido"):
        info = CRITERIOS[chave]
        faixa = classificar_faixa(valores[chave], chave)
        print(f"  {info['rotulo']}: {valores[chave]:g} {info['unidade']} | "
              f"faixa: {faixa} | conforto: {classes[chave].upper()}")
    indice: int = calcular_indice_ruido(valores["ruido"])
    print(f"  Índice de ruído: {indice}/100 (0 = silêncio, 100 = muito ruidoso)")
    print(f"\nEstado geral: {geral.upper()} (semáforo {SEMAFORO[geral]})")


def exibir_mesas(sala: Dict[str, Any]) -> None:
    """Mostra a ocupação de cada mesa da sala."""
    for indice, pessoas in enumerate(sala["mesas"]):
        desenho: str = "#" * pessoas + "." * (LUGARES_POR_MESA - pessoas)
        print(f"  Mesa {indice + 1}: {pessoas}/{LUGARES_POR_MESA} "
              f"[{desenho}]  {rotulo_mesa(pessoas)}")


def exibir_menu() -> None:
    """Exibe o menu principal."""
    exibir_cabecalho("MENU PRINCIPAL")
    print("Dados simulados: não representam medições reais.\n")
    print(" 1 - Listar salas")
    print(" 2 - Consultar uma sala")
    print(" 3 - Simular entrada/saída de pessoas em uma mesa")
    print(" 4 - Alterar condições ambientais (simulação)")
    print(" 5 - Recomendar sala por atividade")
    print(" 6 - Filtrar salas")
    print(" 7 - Salvar dados (JSON)")
    print(" 8 - Carregar dados (JSON)")
    print(" 9 - Restaurar dados de demonstração")
    print("10 - Manual de utilização")
    print(" 0 - Sair")


def escolher_sala(salas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Mostra as salas numeradas e retorna a sala escolhida (número ou ID)."""
    exibir_tabela(salas)
    print()
    while True:
        sala = buscar_sala(salas, ler_texto("Número ou ID da sala (ex.: 3 ou S03): "))
        if sala is not None:
            return sala
        print("Sala não encontrada. Digite o número da lista ou o ID.")


# ---------------------------------------------------------------------
# FUNCIONALIDADES DO MENU
# ---------------------------------------------------------------------


def opcao_listar(salas: List[Dict[str, Any]]) -> None:
    """Opção 1: lista todas as salas."""
    exibir_cabecalho("LISTA DE SALAS")
    exibir_tabela(salas)
    exibir_resumo(salas)
    exibir_legenda()
    pausar()


def opcao_consultar(salas: List[Dict[str, Any]]) -> None:
    """Opção 2: detalha uma sala escolhida."""
    exibir_cabecalho("CONSULTAR SALA")
    sala = escolher_sala(salas)
    print()
    exibir_detalhe(sala)
    pausar()


def opcao_simular_mesa(salas: List[Dict[str, Any]]) -> None:
    """Opção 3: entrada/saída de pessoas em uma mesa."""
    exibir_cabecalho("SIMULAR ENTRADA/SAÍDA EM MESA")
    sala = escolher_sala(salas)
    while True:
        print(f"\n{sala['id']} - {sala['nome']}")
        exibir_mesas(sala)
        print("\n1 - Entrada de pessoa (+1)")
        print("2 - Saída de pessoa (-1)")
        print("0 - Voltar ao menu")
        acao: int = ler_inteiro("Escolha (0-2): ", 0, 2)
        if acao == 0:
            break
        mesa: int = ler_inteiro(f"Número da mesa (1 a {len(sala['mesas'])}): ",
                           1, len(sala["mesas"]))
        match acao:
            case 1:
                sucesso, mensagem = alterar_mesa(sala, mesa - 1, 1)
            case _:
                sucesso, mensagem = alterar_mesa(sala, mesa - 1, -1)
        if sucesso:
            ESTADO["alterado"] = True
        print(mensagem)


def opcao_ambiente(salas: List[Dict[str, Any]]) -> None:
    """Opção 4: altera temperatura, luminosidade ou ruído simulados."""
    exibir_cabecalho("ALTERAR CONDIÇÕES AMBIENTAIS (SIMULAÇÃO)")
    sala = escolher_sala(salas)
    print("\n1 - Temperatura\n2 - Luminosidade\n3 - Ruído\n0 - Voltar")
    escolha: int = ler_inteiro("Escolha (0-3): ", 0, 3)
    match escolha:
        case 1:
            chave = "temperatura"
        case 2:
            chave = "luz"
        case 3:
            chave = "ruido"
        case _:
            return
    info = CRITERIOS[chave]
    minimo, maximo = info["leitura"]
    print(f"\nValor atual: {sala[chave]:g} {info['unidade']}")
    novo: float = ler_decimal(f"Novo valor ({minimo:g} a {maximo:g}): ", minimo, maximo)
    sala[chave] = novo
    ESTADO["alterado"] = True
    classe: str = classificar_valor(novo, info["limites"])
    faixa: str = classificar_faixa(novo, chave)
    print(f"Valor de {info['rotulo'].lower()} atualizado para {novo:g} "
          f"{info['unidade']} | faixa: {faixa} | conforto: {classe.upper()}.")
    pausar()


def opcao_recomendar(salas: List[Dict[str, Any]]) -> None:
    """Opção 5: ranking de salas conforme a atividade escolhida."""
    exibir_cabecalho("RECOMENDAR SALA POR ATIVIDADE")
    for numero in ATIVIDADES:
        print(f"{numero} - {ATIVIDADES[numero][1]}")
    print("0 - Voltar")
    escolha: int = ler_inteiro("Escolha (0-3): ", 0, 3)
    if escolha == 0:
        return
    atividade, nome = ATIVIDADES[escolha]
    ranking, excluidas = montar_ranking(salas, atividade)
    print(f"\nRanking para: {nome}")
    print(descrever_regra(atividade))
    print("-" * LARGURA)
    if len(ranking) == 0:
        print("Nenhuma sala disponível para esta atividade agora.")
    else:
        print(f"{'Pos.':<6}{'Pontos':<8}" + cabecalho_tabela())
        print("-" * LARGURA)
        for posicao, item in enumerate(ranking, start=1):
            sala = item["sala"]
            print(f"{posicao:<6}{item['pontos']:<8}" + formatar_linha(sala))
            print(" " * 14 + "Critérios: " + descrever_criterios(sala, atividade))
        melhor = ranking[0]["sala"]
        print(f"\nMelhor opção: {melhor['id']} - {melhor['nome']}")
        print("Desempate: menor ocupação, mais mesas livres e ID.")
    if len(excluidas) > 0:
        print("\nSalas não indicadas:")
        for sala, motivo in excluidas:
            print(f"  {sala['id']} - {motivo}")
    print("\nA pontuação (0 a 100) é didática e usa os limites aprovados pelo grupo.")
    pausar()


def exibir_filtros_ativos(filtros: Dict[str, Tuple[Optional[float], Optional[float]]]) -> None:
    """Mostra os filtros atualmente definidos."""
    print("Filtros ativos:")
    if len(filtros) == 0:
        print("  (nenhum)")
    for chave in filtros:
        minimo, maximo = filtros[chave]
        texto_min: str = "-" if minimo is None else f"{minimo:g}"
        texto_max: str = "-" if maximo is None else f"{maximo:g}"
        print(f"  {FILTROS_INFO[chave][0]}: de {texto_min} até {texto_max}")


def ler_faixa(chave: str) -> Tuple[Optional[float], Optional[float]]:
    """Lê um intervalo (mínimo, máximo) para o filtro; ENTER ignora."""
    rotulo, unidade, limite_min, limite_max = FILTROS_INFO[chave]
    print(f"\n{rotulo} ({unidade}): valores de {limite_min} a {limite_max}.")
    print("Pressione ENTER para ignorar um dos limites.")
    while True:
        minimo = ler_decimal_opcional("  Valor mínimo: ", limite_min, limite_max)
        maximo = ler_decimal_opcional("  Valor máximo: ", limite_min, limite_max)
        if minimo is not None and maximo is not None and minimo > maximo:
            print("O mínimo não pode ser maior que o máximo. Tente novamente.")
        else:
            return (minimo, maximo)


def opcao_filtrar(salas: List[Dict[str, Any]]) -> None:
    """Opção 6: filtros manuais por faixas de valores (inclusivas)."""
    filtros: Dict[str, Tuple[Optional[float], Optional[float]]] = {}
    while True:
        exibir_cabecalho("FILTRAR SALAS")
        exibir_filtros_ativos(filtros)
        print("\n1 - Ocupação total da sala")
        print("2 - Mesas totalmente livres")
        print("3 - Temperatura")
        print("4 - Luminosidade")
        print("5 - Ruído")
        print("6 - Ver resultado")
        print("7 - Limpar filtros")
        print("0 - Voltar ao menu")
        opcao: int = ler_inteiro("Escolha (0-7): ", 0, 7)
        match opcao:
            case 1 | 2 | 3 | 4 | 5:
                chave = OPCOES_FILTRO[opcao]
                faixa = ler_faixa(chave)
                if faixa == (None, None):
                    filtros.pop(chave, None)
                else:
                    filtros[chave] = faixa
            case 6:
                resultado = filtrar_salas(salas, filtros)
                print(f"\n{len(resultado)} sala(s) encontrada(s):\n")
                if len(resultado) == 0:
                    print("Nenhuma sala atende a todos os filtros.")
                else:
                    exibir_tabela(resultado, numerar=False)
                pausar()
            case 7:
                filtros = {}
            case _:
                break


def opcao_salvar() -> None:
    """Opção 7: salva os dados no JSON."""
    exibir_cabecalho("SALVAR DADOS")
    salvar_estado()
    pausar()


def opcao_carregar() -> None:
    """Opção 8: carrega os dados do JSON."""
    exibir_cabecalho("CARREGAR DADOS")
    if ESTADO["alterado"]:
        pergunta: str = "Há alterações não salvas que serão perdidas. Continuar? (S/N): "
        if not perguntar_sim_nao(pergunta):
            return
    salas, mensagem = carregar_json()
    if salas is None:
        print(f"Erro: {mensagem} Os dados atuais foram mantidos.")
    else:
        ESTADO["salas"] = salas
        ESTADO["alterado"] = False
        print(mensagem)
    pausar()


def opcao_restaurar() -> None:
    """Opção 9: restaura os dados de demonstração."""
    exibir_cabecalho("RESTAURAR DADOS DE DEMONSTRAÇÃO")
    pergunta: str = "Isso substitui os dados atuais (na memória). Continuar? (S/N): "
    if perguntar_sim_nao(pergunta):
        ESTADO["salas"] = criar_salas_demo()
        ESTADO["alterado"] = True
        print("Dados de demonstração restaurados. Use a opção 7 para salvar.")
    pausar()


def opcao_manual() -> None:
    """Opção 10: manual de utilização."""
    exibir_cabecalho("MANUAL DE UTILIZAÇÃO")
    print("O Study Comfort ajuda a escolher a melhor sala de estudo.")
    print("\n- Cada sala tem mesas com 3 lugares. Grupo e vídeo exigem uma mesa")
    print("  totalmente livre (lugar vago em mesa ocupada não conta).")
    print("- Limite de ruído para indicar a sala: 65 dB simulados no grupo e")
    print("  45 dB no vídeo. Nas salas grandes, a simulação mantém uma mesa livre.")
    print("- Cada grandeza tem duas leituras: a FAIXA (ex.: baixa/média/alta), que")
    print("  só indica onde o valor está, e o CONFORTO (ADEQUADO, ATENÇÃO ou")
    print("  CRÍTICO). Valores muito baixos ou muito altos também podem ser")
    print("  inadequados. O índice de ruído vai de 0 (silêncio) a 100.")
    print("- O estado geral segue o semáforo: vermelho se algum item é")
    print("  crítico; amarelo se há atenção; verde se tudo é adequado.")
    print("- Ao escolher uma sala, digite o número da lista ou o ID (S03).")
    print("- Use as opções 3 e 4 para simular mudanças e a opção 5 para")
    print("  ver o ranking por atividade (desempate: menor ocupação, mais")
    print("  mesas livres e ID). A opção 6 filtra por faixas.")
    print("- Salve (opção 7) para manter as alterações no arquivo JSON.")
    print("- Digite SAIR em qualquer tela para encerrar (com confirmação).")
    print("\nAtenção: todos os dados são simulados ou fictícios.")
    pausar()


# ---------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------


def main() -> None:
    """Executa o laço principal do menu."""
    exibir_cabecalho("INICIALIZAÇÃO")
    inicializar_dados()
    pausar()
    while True:
        exibir_menu()
        opcao: int = ler_inteiro("\nEscolha uma opção (0-10): ", 0, 10)
        salas = ESTADO["salas"]
        match opcao:
            case 1:
                opcao_listar(salas)
            case 2:
                opcao_consultar(salas)
            case 3:
                opcao_simular_mesa(salas)
            case 4:
                opcao_ambiente(salas)
            case 5:
                opcao_recomendar(salas)
            case 6:
                opcao_filtrar(salas)
            case 7:
                opcao_salvar()
            case 8:
                opcao_carregar()
            case 9:
                opcao_restaurar()
            case 10:
                opcao_manual()
            case 0:
                solicitar_saida()