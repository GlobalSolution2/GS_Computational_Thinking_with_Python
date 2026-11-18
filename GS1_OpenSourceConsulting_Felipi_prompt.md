# Uso de Inteligência Artificial: Study Comfort

**Global Solution 2026.2 · FIAP · Computational Thinking with Python**
Equipe **Open Source Consulting** · Daniel Roberto (RM 571746), Felipe Pedrol (RM 569631), Jecky Cossio (RM 572226) e Felipi Godoy (RM 573741)

## 1. Ferramentas utilizadas

| Ferramenta | Finalidade |
|---|---|
| **Claude** (Anthropic) | Auxílio pontual como copiloto técnico para estruturação inicial do menu, tratamento de exceções, validação de arquivos JSON e diretrizes para a divisão modular do código (`main.py`, `interface.py`, `dados.py` e `regras.py`). |
| **Gemini** & **ChatGPT** | Uso exploratório para comparação de ideias sobre a modelagem das regras ambientais e análise de robustez das estruturas de dados. |

## 2. Exemplos representativos de interações

Os exemplos resumem os pedidos e as orientações discutidas, sem reproduzir todas as mensagens ou os textos exatos.

### 2.1. Claude: auxílio na lógica e validação do JSON

#### Exemplo 1: tratamento de exceções e integridade de arquivos

**Prompt representativo:**
> Estou desenvolvendo a aplicação em Python do projeto Study Comfort e preciso implementar a leitura e gravação em JSON com validação estrita (verificando campos obrigatórios, IDs repetidos sem diferenciação de maiúsculas/minúsculas e restrição de salas grandes). Como posso estruturar essa função em Python puro, tratando erros de arquivo corrompido sem derrubar o programa?

**Resumo da resposta:**
A ferramenta sugeriu blocos estruturados com `try/except` para capturar `FileNotFoundError` e `ValueError`, além de funções lógicas para varrer a lista de salas e conferir os limites estabelecidos pela equipe.

**Aplicação no projeto:**
O código foi adaptado, testado e integrado pela equipe, garantindo que o programa abra com dados de demonstração em caso de falha no JSON sem interromper a execução no terminal.

### 2.2. Claude: modularização do código

#### Exemplo 2: divisão em múltiplos arquivos sem dependência circular

**Prompt representativo:**
> Desenvolvi o código principal em arquivo único, mas a arquitetura pode ser organizada em módulos (`main`, `interface`, `dados`, `regras`). Como posso dividir o código em quatro arquivos mantendo a mesma lógica e evitando dependências circulares em Python?

**Resumo da resposta:**
Apresentou um plano de separação de responsabilidades: `regras.py` contendo apenas funções puras (sem I/O), `dados.py` gerenciando o estado e o JSON, `interface.py` cuidando das telas e menus, e o `main.py` como ponto de entrada.

**Aplicação no projeto:**
A equipe revisou a proposta, organizou os arquivos na mesma pasta e validou os 13 cenários de teste para garantir que a modularização não alterasse o comportamento funcional do programa.

## 3. Validação das orientações

Todo o código desenvolvido foi construído com a liderança e autoria da equipe. As sugestões obtidas pelas ferramentas de IA serviram como suporte técnico para refinar trechos específicos, como a validação de formato e a sintaxe de blocos `match/case`. 

Após receber orientações ou rascunhos de funções, a equipe implementou os códigos, realizou testes manuais rigorosos com os 13 casos do roteiro e conferiu os resultados matemáticos do ranking de recomendação frente a um gabarito independente. Nenhuma sugestão foi aplicada cegamente; todas passaram por validação prática no PyCharm.

## 4. Análise crítica

**Benefícios:** O uso pontual de IA auxiliou a acelerar o desenvolvimento de estruturas repetitivas de validação e ofereceu caminhos limpos para a divisão modular do código, garantindo a organização exigida para a entrega.

**Limitações e Aprendizados:** Percebemos que confiar cegamente em códigos gerados por IA pode introduzir complexidades desnecessárias ou quebras de escopo. A equipe manteve o controle total do projeto, adaptando as sugestões às regras de negócio reais definidas pelo grupo e restringindo o uso às bibliotecas padrão permitidas (`json` e `os`).