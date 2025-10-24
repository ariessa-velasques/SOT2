# Simulador de Gerenciamento de Memória com Paginação

Este projeto é uma implementação em Python de um simulador de gerenciamento de memória virtual com paginação, desenvolvido para a disciplina de Sistemas Operacionais.

## O que é o Trabalho?

O objetivo é simular o comportamento do gerenciamento de memória em um sistema operacional. A simulação inclui os seguintes conceitos:

-   **Memória Virtual:** Um espaço de endereçamento lógico dividido em páginas.
-   **Memória Física:** Um espaço de armazenamento real dividido em quadros (frames).
-   **Tabela de Páginas:** Uma estrutura de dados que mapeia as páginas virtuais para os quadros da memória física.
-   **Falha de Página (Page Fault):** Ocorre quando um programa tenta acessar uma página que não está carregada na memória física.
-   **Algoritmo de Substituição de Página:** Quando a memória física está cheia e uma nova página precisa ser carregada, um algoritmo decide qual página antiga deve ser removida. Este simulador implementa o **FIFO (First-In, First-Out)**.

## Como Funciona?

O simulador (`simulador.py`) implementa a lógica de gerenciamento de memória com as seguintes características:

1.  **Inicialização Interativa:** O programa solicita ao usuário que defina a configuração da simulação:
    -   O tamanho da memória física (em número de quadros).
    -   O tamanho da memória virtual (em número de páginas).
    -   A sequência de acesso (uma string de números separados por espaço).

2.  **Simulação de Acesso:** O programa processa a sequência de acessos, um por um. Para cada acesso:
    -   Ele consulta a **Tabela de Páginas** para verificar se a página está na memória física (um *hit*).
    -   Se a página não estiver presente, ocorre uma **Falha de Página** (*page fault*).

3.  **Tratamento de Falha de Página:**
    -   O simulador procura por um quadro livre na memória física para carregar a nova página.
    -   Se a memória física estiver cheia, o algoritmo de substituição **FIFO** é acionado para escolher uma página a ser removida (a que entrou primeiro).
    -   A Tabela de Páginas é atualizada para refletir o novo estado da memória.

4.  **Saída Detalhada:** A cada passo da simulação, o programa exibe um relatório claro do estado atual, incluindo:
    -   O conteúdo da Memória Física (quadros).
    -   O estado da fila do algoritmo FIFO.
    -   Um **mapeamento explícito** que mostra qual Página Virtual está em qual Quadro Físico (ex: `Página 5 -> Quadro 0`).

5.  **Relatório Final:** Ao final da execução, ele apresenta um **relatório estatístico completo**, incluindo o total de acessos, o número de *hits*, o número de *page faults* e as taxas percentuais de acerto e falha.

### Como Executar

O programa é interativo. Para rodar a simulação, basta executar o script Python em um terminal e fornecer os dados quando solicitado:

```bash
python simulador.py
```

## Casos de Teste para Validação

Esta seção contém uma suíte de testes projetada para validar a funcionalidade e a robustez do simulador. Cada teste foca em um aspecto específico do comportamento do algoritmo FIFO.

### Categoria 1: Testes de Funcionalidade Básica

#### Teste 1: Sequência Vazia
* **Objetivo:** Garantir que o programa lida com uma entrada vazia (sem acessos) de forma robusta e sem erros.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `10`
    * Sequência de Acesso: `` (pressione Enter)
* **Análise Esperada:** O programa deve iniciar e finalizar imediatamente, exibindo o relatório final com 0 acessos, 0 *Page Faults* e 0 *Hits*. Isso prova que o programa lida com casos nulos.

---

#### Teste 2: Sem Substituição (Memória Suficiente)
* **Objetivo:** Verificar o preenchimento inicial da memória quando o número de páginas acessadas é menor ou igual ao número de quadros.
* **Parâmetros:**
    * Memória Física: `5`
    * Memória Virtual: `10`
    * Sequência de Acesso: `0 1 2 3`
* **Análise Esperada:** Devem ocorrer exatamente 4 *Page Faults*. Nenhuma substituição deve ocorrer, pois há espaço livre. A fila FIFO deve conter `[0, 1, 2, 3]`. Isso testa as "falhas compulsórias" (compulsory misses).

---

#### Teste 3: Substituição Simples
* **Objetivo:** Confirmar a lógica básica do FIFO com uma única substituição.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `5`
    * Sequência de Acesso: `0 1 2 3`
* **Análise Esperada:** Devem ocorrer 4 *Page Faults*. Os 3 primeiros acessos preenchem a memória (`[0, 1, 2]`). Ao acessar a página `3`, a memória está cheia, e o FIFO deve remover a página `0` (a "First-In"). A memória final será `[3, 1, 2]` e a fila `[1, 2, 3]`.

### Categoria 2: Testes de Comportamento do Algoritmo

#### Teste 4: Alta Localidade de Referência
* **Objetivo:** Simular um programa que acessa repetidamente um pequeno conjunto de páginas. A taxa de *hits* deve ser alta após o "aquecimento" inicial.
* **Parâmetros:**
    * Memória Física: `4`
    * Memória Virtual: `10`
    * Sequência de Acesso: `1 2 3 1 2 1 2 3 1 2`
* **Análise Esperada:** Os 3 primeiros acessos (`1 2 3`) serão *Page Faults*. Os 7 acessos seguintes (`1 2 1 2 3 1 2`) devem ser todos *Hits*, pois as páginas estão na memória. O relatório final deve mostrar **3 Page Faults** e **7 Hits**, provando que a lógica do "bit de presença" e o contador de *hits* funcionam.

---

#### Teste 5: Anomalia de Belady (Parte A)
* **Objetivo:** Estabelecer a linha de base de falhas com uma quantidade menor de memória física, para o caso clássico da anomalia.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `5`
    * Sequência de Acesso: `0 1 2 3 0 1 4 0 1 2 3 4`
* **Análise Esperada:** O resultado final deve ser de **9 Page Faults**. Anote este número para comparação com o próximo teste.

---

#### Teste 6: Anomalia de Belady (Parte B)
* **Objetivo:** Demonstrar que, com FIFO, aumentar a memória física pode, paradoxalmente, aumentar o número de falhas de página.
* **Parâmetros:**
    * Memória Física: `4` (um quadro a mais que o Teste 5)
    * Memória Virtual: `5`
    * Sequência de Acesso: `0 1 2 3 0 1 4 0 1 2 3 4` (mesma sequência)
* **Análise Esperada:** O número de *Page Faults* deve ser **10**. Este resultado (10 falhas com 4 quadros) é pior do que o do Teste 5 (9 falhas com 3 quadros), comprovando que o simulador reproduz corretamente a Anomalia de Belady.

---

#### Teste 7: Pior Caso para o FIFO (Varredura Circular)
* **Objetivo:** Explorar o cenário de pior desempenho do FIFO, onde a página necessária é sempre a que acabou de ser removida.
* **Parâmetros:**
    * Memória Física: `4`
    * Memória Virtual: `10`
    * Sequência de Acesso: `0 1 2 3 4 0 1 2 3 4 0 1 2 3 4`
* **Análise Esperada:** O conjunto de páginas acessadas (5 páginas: 0,1,2,3,4) é ligeiramente maior que a memória física (4 quadros). Isso causa "thrashing": após os 4 primeiros *faults*, **cada acesso subsequente resultará em um *page fault***, levando a uma taxa de falhas altíssima (12 *faults* em 14 acessos).

### Categoria 3: Testes de Casos Limítrofes (Edge Cases)

#### Teste 8: Memória com Apenas Um Quadro
* **Objetivo:** Testar o comportamento em uma condição de recurso extremamente limitado.
* **Parâmetros:**
    * Memória Física: `1`
    * Memória Virtual: `10`
    * Sequência de Acesso: `0 1 0 2 0 3`
* **Análise Esperada:** Cada acesso a uma página diferente da que está na memória resultará em um *Page Fault*. Os acessos à página `0` serão *hits* (se ela for a última acessada) ou *faults* (se outra página a removeu). A memória física simplesmente alternará entre as páginas.

---

#### Teste 9: Acessos Consecutivos à Mesma Página
* **Objetivo:** Garantir que acessos repetidos à mesma página resultem em *hits* após a primeira falha.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `10`
    * Sequência de Acesso: `7 7 7 7 7`
* **Análise Esperada:** O resultado deve ser exatamente **1 Page Fault** (na primeira vez que a página 7 é acessada) e **4 Hits**. Isso valida o contador de *hits* e a lógica de verificação.

---

#### Teste 10: Acesso a Página Inválida
* **Objetivo:** Confirmar que o tratamento de erro para acessos fora do limite da memória virtual está funcionando.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `5` (Páginas válidas são 0, 1, 2, 3, 4)
    * Sequência de Acesso: `0 1 2 99 3 4 10`
* **Análise Esperada:** O programa não deve quebrar. Ele deve exibir o aviso "AVISO: Acesso à página virtual inválida 99. Ignorando." e depois "AVISO: Acesso à página virtual inválida 10. Ignorando.". A simulação deve continuar normalmente com as páginas válidas (`0, 1, 2, 3, 4`).