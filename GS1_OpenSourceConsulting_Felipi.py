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
ARQUIVO     : GS1_OpenSourceConsulting_Felipi.py
VERSÃO      : 1.1 (modularizada com type hints)
DESCRIÇÃO   : Simulador em terminal de salas de estudo. Ajuda estudantes a
              escolher o ambiente mais adequado (ocupação, mesas livres,
              temperatura, luminosidade e ruído). Todos os dados são
              simulados/fictícios e não representam medições reais.
ATIVIDADE   : Aplicação Python - Global Solution 2026.2 (CitizenTech)
=====================================================================
"""

from GS1_OpenSourceConsulting_Felipi_interface import main

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrompido pelo usuário.")