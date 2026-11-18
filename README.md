# Study Comfort — Aplicação Python

**Global Solution 2026.2 · FIAP · Engenharia de Software, 1º ano · Computational Thinking with Python**
Equipe **Open Source Consulting** · Programa modularizado (`main.py`, `interface.py`, `dados.py` e `regras.py`), versão 1.1

> Todos os dados deste programa são **simulados ou fictícios**. Nenhuma sala física foi medida e nenhum dado pessoal é utilizado.

---

## Ficha CitizenTech

| Campo | Definição |
|---|---|
| **Nome da CitizenTech** | Study Comfort |
| **Cidade e bairro** | São Paulo/SP |
| **Cidadão beneficiado** | Estudantes universitários que querem escolher um ambiente adequado para estudar, trabalhar em grupo ou gravar vídeos/projetos. |
| **Problema, em uma frase** | Estudantes têm dificuldade para identificar, antes de se deslocar, salas com espaço e condições adequadas de ruído, temperatura e luminosidade para suas atividades. |
| **Como funciona** | O fluxo da S01 (Sala 1) é ESP32 simulado no Wokwi → Supabase → painel React. A conexão local está configurada e a leitura pelo painel foi validada. S02 a S09 usam simulações locais. O painel oferece filtros, recomendações, favoritos locais e listas compartilhadas no Supabase. |
| **O que cada parte faz** | Edge: leitura simulada e decisão local (LEDs); Supabase: guarda o histórico da sala IoT e as listas compartilhadas; React/Web: exibição, filtros, rankings e CRUD de listas pela API. |
| **Link do repositório** | https://github.com/GlobalSolution2/GS_Web_Front_Open_Source_Consulting |
| **Indicador de impacto** | Novas entrevistas com os usuários da plataforma, perguntando quanto tempo provavelmente foi economizado através do uso da plataforma, e quantas vezes por seman é usado a plataforma pelo usuário. |
| **ODS conectados** | **ODS 4:** Educação de Qualidade (principal: melhores condições para estudar); **ODS 9:** Indústria, Inovação e Infraestrutura (apoio: IoT aplicada à infraestrutura do campus); possivelmente **ODS 11:** Cidades e Comunidades Sustentáveis (uso eficiente de espaços coletivos). |

### Equipe

| Integrante | RM |
|---|---|
| Daniel Roberto | 571746 |
| Felipe Pedrol | 569631 |
| Jecky Cossio | 572226 |
| Felipi Bandeira de Godoy | 573741 |

---

## 1. O problema e o papel do Python

As entrevistas com estudantes registraram **tempo de procura e desconforto**: cinco relatos qualitativos (três do Mackenzie e dois da FIAP) citam salas barulhentas, frias ou cheias e mesas parcialmente ocupadas que não servem a um grupo. Um dos relatos estima cerca de 10 minutos por dia de procura, sendo uma estimativa individual, sem cronometragem. Os relatos são qualitativos, sem amostragem representativa, e **não comprovam benefício** da solução.

A **necessidade identificada** é conhecer ocupação, ruído, temperatura e iluminação **antes** de se deslocar, para escolher uma sala conforme a atividade e as preferências de cada pessoa.

O papel desta parte do projeto, segundo a disciplina, é uma aplicação em Python responsável por **processar dados e tomar decisões**. O programa:

- guarda o estado de nove salas (mesas, temperatura, luz e ruído) em arquivo JSON;
- classifica cada grandeza de duas formas: a **faixa** (onde o valor está) e o **conforto** (adequado, atenção ou crítico);
- resume cada sala em um semáforo (verde, amarelo ou vermelho);
- simula entradas e saídas de pessoas nas mesas e mudanças nas condições ambientais;
- **recomenda** a melhor sala para três atividades: estudar sozinho, trabalhar em grupo e gravar vídeo;
- filtra as salas por faixas de valores.

O Python é **independente** do Wokwi, do Supabase e do site: usa os mesmos limites e as mesmas regras, mas não troca dados com eles.

## 2. Como executar

**Requisitos:** Python 3.10 ou superior (o programa usa `match/case`). Não é preciso instalar nenhuma biblioteca: são usados apenas os módulos `json` e `os`, da instalação padrão.

**No PyCharm:** abra a pasta com os quatro arquivos `.py`, abra o arquivo principal de lançamento e execute (Run). O programa funciona no terminal integrado. **Os quatro arquivos devem permanecer na mesma pasta.**

**No terminal:**

```bash
python GS1_OpenSourceConsulting_Felipi.py
```

Na primeira execução, o programa cria o arquivo `dados_study_comfort.json` na mesma pasta, com os dados de demonstração. Nas execuções seguintes, ele carrega esse arquivo.

**Comando global:** digitar `SAIR` (com ou sem maiúsculas) em qualquer tela pede confirmação S/N e encerra o programa, oferecendo salvar alterações pendentes.

## 3. Menu principal

| Opção | Função |
|---|---|
| 1 | **Listar salas:** tabela com ocupação, mesas livres, temperatura, luz, ruído e estado, mais um resumo consolidado e o semáforo geral |
| 2 | **Consultar uma sala:** detalhes, mesas, faixa e conforto de cada grandeza e índice de ruído. A sala pode ser escolhida pelo número (3) ou pelo ID (S03) |
| 3 | **Simular entrada/saída em uma mesa:** soma ou subtrai uma pessoa, respeitando os limites |
| 4 | **Alterar condições ambientais:** muda temperatura, luz ou ruído simulados e mostra a nova classificação |
| 5 | **Recomendar sala por atividade:** ranking para estudar sozinho, trabalhar em grupo ou gravar vídeo, com a explicação dos critérios e das salas não indicadas |
| 6 | **Filtrar salas:** filtros combináveis por ocupação, mesas livres, temperatura, luz e ruído |
| 7 | **Salvar dados** em JSON |
| 8 | **Carregar dados** do JSON |
| 9 | **Restaurar** os dados de demonstração |
| 10 | **Manual de utilização** |
| 0 | **Sair** (com confirmação) |

### Roteiro rápido de demonstração

1. Opção **1** para ver as nove salas e o semáforo.
2. Opção **5**, atividade **2** (grupo): a S07 aparece em primeiro lugar.
3. Opção **3**, sala **S08**, mesa 4, entrada: o programa recusa, pois a sala grande deve manter uma mesa livre.
4. Opção **4**, sala **S02**, ruído **70**: o conforto passa a CRÍTICO, e a sala deixa de ser indicada para grupo.
5. Opção **7** para salvar e `SAIR` para encerrar.

## 4. Regras de negócio

### 4.1 Mesas e salas

- Cada mesa tem **3 lugares** e abriga de 0 a 3 pessoas. Capacidade da sala = mesas × 3.
- Porte: 2 mesas (pequena, 6 lugares), 3 mesas (média, 9 lugares) e 4 mesas (grande, 12 lugares).
- Uma mesa só é **totalmente livre** se não tiver ninguém sentado. Lugares vagos em mesa ocupada não contam para grupo nem para vídeo.
- **Salas grandes** mantêm sempre pelo menos uma mesa totalmente livre (no máximo 9 pessoas). O programa recusa uma entrada que violaria isso e rejeita arquivos JSON que a violem.

### 4.2 Limites das condições (tabela única do grupo)

Os limites vieram da tabela única de limiares do grupo, aprovada por todos. As comparações são **estritas** (`<` e `>`): o próprio limite fica do lado de dentro. Por exemplo, 18 °C é atenção (não crítico) e 45 dB é adequado.

| Indicador | Adequado | Atenção | Crítico | Faixa: baixa / média / alta |
|---|---|---|---|---|
| Temperatura (°C) | 21 a 25 | 18 até menos de 21, ou acima de 25 até 26 | abaixo de 18 ou acima de 26 | abaixo de 21 / 21 a 26 / acima de 26 |
| Luz (lux estimado) | 300 a 2000 | 200 até menos de 300, ou acima de 2000 até 3000 | abaixo de 200 ou acima de 3000 | abaixo de 300 / 300 a 750 / acima de 750 |
| Ruído (dB simulados) | até 45 | acima de 45 até 65 | acima de 65 | silencioso (abaixo de 40) / moderado (40 a 55) / barulhento (acima de 55) |
| Ocupação (% dos lugares) | até 50 | acima de 50 até 90 | acima de 90 | abaixo de 35 / 35 a 70 / acima de 70 |

- No ruído e na ocupação só o lado alto gera alerta: pouco barulho e sala vazia não são problema.
- A **faixa** só indica onde o valor está. O **conforto** diz se a sala está boa para uso. Uma temperatura de 24 °C, por exemplo, está na faixa média e é adequada, enquanto 26 °C está na faixa média e é atenção.
- **Estado geral (semáforo):** vermelho se algum indicador for crítico; amarelo se nenhum for crítico e ao menos um estiver em atenção; verde se todos forem adequados.
- **Índice de ruído:** de 0 (30 dB simulados) a 100 (80 dB simulados), calculado por `2 × (dB − 30)` e limitado entre 0 e 100. O meio arredonda para cima.
- **Leituras possíveis:** temperatura de −40 a 80 °C, luz de 0 a 100000 lux e ruído de 30 a 80 dB simulados. Fora disso a leitura é impossível, e o programa a recusa.
- O ruído é **simulado** (dB simulados) e a luz é um **lux estimado**: o programa não mede som nem luz reais.

### 4.3 Recomendação por atividade

Cada atividade exige condições mínimas para a sala ser indicada e pontua os demais critérios (soma 100):

| Critério | Estudar sozinho | Trabalho em grupo | Gravar vídeo |
|---|---:|---:|---:|
| Ruído | 40 | 20 | 35 |
| Temperatura | 20 | 10 | 0 |
| Luz | 20 | 10 | 10 |
| Lugares vagos | 20 | 25 | 20 |
| Mesas totalmente livres | 0 | 35 | 35 |
| **Exigência para ser indicada** | ao menos um lugar vago | mesa totalmente livre e ruído até 65 dB | mesa totalmente livre e ruído até 45 dB |

Como a pontuação é calculada:

- **Ruído, temperatura e luz:** peso inteiro se adequado, metade se atenção e zero se crítico. No vídeo, o ruído pontua pelo **silêncio**: peso inteiro até 30 dB, caindo em linha reta até zero em 45 dB.
- **Lugares vagos:** proporcional à capacidade da sala.
- **Mesas livres:** cada mesa vale um quarto do peso, até quatro mesas.
- O resultado é arredondado, e o meio ponto sobe (21,5 vira 22).
- **Desempate:** menor taxa de ocupação, depois mais mesas totalmente livres e, por fim, o ID da sala.
- Gravar vídeo significa trabalhos ou apresentações acadêmicas. **Não há reserva** nem exclusividade da sala. A pontuação é didática e serve para comparar salas.

## 5. Dados e arquivo JSON

O arquivo `dados_study_comfort.json` guarda as salas. Exemplo de uma sala:

```json
{
    "schema_version": 1,
    "salas": [
        {
            "id": "S07",
            "nome": "Sala de Estudo 07",
            "mesas": [0, 0, 1],
            "temperatura": 23.0,
            "luz": 450,
            "ruido": 39,
            "fonte": "Dados demonstrativos"
        }
    ]
}
```

- `mesas` é a lista de pessoas sentadas em cada mesa (0 a 3).
- Ao carregar, o programa **valida** o arquivo: estrutura, campos obrigatórios, tipos, IDs repetidos (sem diferenciar maiúsculas de minúsculas), mesas, leituras possíveis e a regra das salas grandes. Arquivo ausente, corrompido ou inválido **não derruba** o programa: ele avisa, usa os dados de demonstração e só substitui o arquivo se o usuário salvar.

### Salas de demonstração

As salas S02 a S09 seguem o cenário fictício do grupo. A S01 usa o exemplo do contrato de dados do projeto. A S09 foi ajustada para respeitar a regra das salas grandes (uma mesa livre).

| Sala | Mesas | Temp. (°C) | Luz (lux) | Ruído (dB) | Estado |
|---|---|---:|---:|---:|---|
| S01 | [1, 2, 0] | 22,8 | 410 | 54 | Atenção |
| S02 | [0, 2] | 22 | 410 | 42 | Adequado |
| S03 | [3, 3] | 18 | 920 | 71 | Crítico |
| S04 | [1, 1, 1] | 21 | 500 | 46 | Atenção |
| S05 | [0, 3, 3] | 24 | 350 | 57 | Atenção |
| S06 | [2, 2, 1] | 19 | 180 | 61 | Crítico |
| S07 | [0, 0, 1] | 23 | 450 | 39 | Adequado |
| S08 | [3, 2, 1, 0] | 25 | 600 | 53 | Atenção |
| S09 | [3, 3, 3, 0] | 28 | 760 | 68 | Crítico |

## 6. Requisitos da disciplina e onde estão no código

| Requisito | Onde aparece (arquivo e função) |
|---|---|
| Menu de opções | `GS1_OpenSourceConsulting_Felipi_interface.py`: `exibir_menu` e laço principal em `main`, com `match/case` |
| Validação de entradas | `GS1_OpenSourceConsulting_Felipi_interface.py`: `ler_inteiro`, `ler_decimal`, `ler_decimal_opcional` e `perguntar_sim_nao`. `GS1_OpenSourceConsulting_Felipi_regras.py`: `buscar_sala`. `GS1_OpenSourceConsulting_Felipi_dados.py`: `validar_dados` |
| Tratamento de exceções (`try/except`) | `GS1_OpenSourceConsulting_Felipi_interface.py`: `ler_inteiro` e `ler_decimal`. `GS1_OpenSourceConsulting_Felipi_regras.py`: `buscar_sala`. `GS1_OpenSourceConsulting_Felipi_dados.py`: `salvar_json` e `carregar_json` |
| `if/elif/else` | `GS1_OpenSourceConsulting_Felipi_regras.py`: `classificar_valor`, `classificar_faixa`, `estado_geral`, `tipo_sala`, `rotulo_mesa` e `alterar_mesa` |
| `match/case` | `GS1_OpenSourceConsulting_Felipi_interface.py`: `main`, `opcao_simular_mesa`, `opcao_ambiente`, `opcao_filtrar`, `descrever_criterios`, `descrever_regra` e `perguntar_sim_nao` |
| `while` e `for` | `while`: laços de leitura e do menu. `for`: tabelas, resumo, filtros, ranking e validação |
| Funções com parâmetros e retorno | Todas as funções; por exemplo `GS1_OpenSourceConsulting_Felipi_regras.py`: `pontuar_sala(sala, atividade)` retorna a pontuação |
| Listas, tuplas e dicionários | Listas: `mesas` e ranking. Tuplas: faixas e limites em `CRITERIOS`, retornos `(ok, mensagem)`. Dicionários: salas, `CRITERIOS`, `PESOS` e `ESTADO` |
| Arquivos JSON (leitura e gravação) | `GS1_OpenSourceConsulting_Felipi_dados.py`: `salvar_json` e `carregar_json`. `GS1_OpenSourceConsulting_Felipi_interface.py`: `inicializar_dados` |
| Boas práticas | Docstring em todas as funções, constantes no topo (`CRITERIOS`, `PESOS`), seções comentadas, nomes claros, funções pequenas e reutilizáveis, divisão em módulos com *type hints*, só `json` e `os` |
| Experiência do usuário | Cabeçalho padrão em toda tela, mensagens claras, manual (opção 10), comando `SAIR` com confirmação e aviso de alterações não salvas |

## 7. Casos de teste

Roteiro com o resultado esperado, usando os dados de demonstração:

| # | Ação | Resultado esperado |
|---|---|---|
| 1 | Opção 4, S02, temperatura **18** | faixa baixa · conforto **ATENÇÃO** |
| 2 | Opção 4, temperatura **26** | faixa média · conforto **ATENÇÃO** |
| 3 | Opção 4, ruído **45** | faixa moderado · conforto **ADEQUADO** |
| 4 | Opção 4, ruído **65** (depois **65,5**) | barulhento, **ATENÇÃO** (depois **CRÍTICO**) |
| 5 | Opção 4, luz **2000** (depois **3000**) | faixa alta, **ADEQUADO** (depois **ATENÇÃO**) |
| 6 | Opção 4, ruído **29** ou **81**, ou temperatura **abc** | valor recusado, com nova tentativa |
| 7 | Opção 3, S03, mesa 1, entrada | recusada: mesa já cheia (3/3) |
| 8 | Opção 3, S08, mesa 4, entrada | recusada: sala grande mantém uma mesa livre |
| 9 | Opção 5, **grupo** | S07 (80), S02 (65), S01 (55), S08 (51), S05 (47) |
| 10 | Opção 5, **vídeo** | S07 (59), S02 (39); as demais não são indicadas por ruído ou falta de mesa livre |
| 11 | Opção 2, digitar `s03` | abre a S03 (ID aceito em maiúscula ou minúscula) |
| 12 | Digitar `SAIR` em qualquer pergunta | confirmação S/N; `N` continua e `S` encerra |
| 13 | Arquivo JSON corrompido ou com IDs `s01` e `S01` | aviso, uso dos dados de demonstração e arquivo preservado |

## 8. Limitações

- Todos os dados são simulados ou fictícios. O programa não mede salas físicas e não se conecta ao Wokwi, ao Supabase nem ao site.
- Os limites e os pesos do ranking vêm da tabela do grupo. Eles usam normas de ambientes de trabalho e de projeto como **referência**, e a ocupação não tem norma, sendo critério do grupo. A pontuação é didática.
- As salas são fixas (nove, com 2, 3 ou 4 mesas). O programa não cadastra nem exclui salas, e não há login nem reserva.
- Nas salas grandes, a simulação fica limitada a 9 pessoas, embora a capacidade física seja de 12 lugares.

## 9. Uso de Inteligência Artificial

Ferramentas de IA foram utilizadas no desenvolvimento. O registro completo (ferramentas, prompts, funcionalidades, validação e análise crítica) está no arquivo correspondente de prompts.

## 10. Estrutura e conteúdo da entrega

O código está dividido em quatro arquivos na **mesma pasta**, sem dependência circular: o arquivo principal (`GS1_OpenSourceConsulting_Felipi.py`) importa a interface, que por sua vez utiliza os módulos de dados e regras.

| Arquivo | Descrição |
|---|---|
| `GS1_OpenSourceConsulting_Felipi.py` | Ponto de entrada: é o arquivo a executar |
| `GS1_OpenSourceConsulting_Felipi_interface.py` | Telas, entrada de dados validada, saída do programa e funcionalidades do menu |
| `GS1_OpenSourceConsulting_Felipi_dados.py` | Salas de demonstração, estado do programa e arquivo JSON (salvar, carregar e validar) |
| `GS1_OpenSourceConsulting_Felipi_regras.py` | Regras de negócio: classificação, ranking e simulação (funções puras, com *type hints*) |
| `GS1_OpenSourceConsulting_Felipi_readme.md` | Este documento (conforme padrão da entrega) |
| `GS1_OpenSourceConsulting_Felipi_prompt.md` | Documentação do uso de IA (conforme padrão da entrega) |

O arquivo `dados_study_comfort.json` é criado automaticamente na primeira execução e não faz parte da entrega individual.

## 11. Arquitetura e evolução

### Estrutura de pastas e módulos

```text
study-comfort/
├── GS1_OpenSourceConsulting_Felipi.py                # ponto de entrada
├── GS1_OpenSourceConsulting_Felipi_interface.py      # telas, entradas e menu
├── GS1_OpenSourceConsulting_Felipi_dados.py          # estado e arquivo JSON
├── GS1_OpenSourceConsulting_Felipi_regras.py         # regras de negócio puras
├── dados_study_comfort.json                          # gerado na primeira execução
├── GS1_OpenSourceConsulting_Felipi_readme.md
└── GS1_OpenSourceConsulting_Felipi_prompt.md
```

### Decisões de projeto

- **`regras.py` é puro:** só funções com *type hints* e constantes, sem entrada/saída, sem arquivo e sem estado. Isso o torna previsível e fácil de testar.
- **`dados.py` guarda o estado:** o dicionário `ESTADO` vive aqui e é alterado apenas pelas chaves, sem ser reatribuído. O módulo não imprime nada na tela.
- **`interface.py` concentra a entrada e a saída:** a leitura validada e a confirmação de saída ficam juntas, porque uma chama a outra (o comando `SAIR` funciona em qualquer pergunta).
- **Mesas/arquivos na mesma pasta:** o caminho do JSON é calculado a partir da pasta de `dados.py`, e todos os arquivos `.py` devem ficar juntos.
