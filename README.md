# Simulador de Gerenciamento de Memória com Paginação

Este projeto é uma implementação em Python de um simulador de gerenciamento de memória virtual com paginação, desenvolvido para a disciplina de Sistemas Operacionais.

## O que é o Trabalho?

O objetivo é simular o comportamento do gerenciamento de memória em um sistema operacional. A simulação inclui os seguintes conceitos:

-   **Memória Virtual:** Um espaço de endereçamento lógico dividido em páginas.
-   **Memória Física:** Um espaço de armazenamento real dividido em quadros (frames).
-   **Tabela de Páginas:** Uma estrutura de dados que mapeia as páginas virtuais para os quadros da memória física.
-   **Falha de Página (Page Fault):** Ocorre quando um programa tenta acessar uma página que não está carregada na memória física.
-   **Algoritmo de Substituição de Página:** Quando a memória física está cheia e uma nova página precisa ser carregada, um algoritmo decide qual página antiga deve ser removida.

## Como Funciona?

O simulador (`simulador.py`) implementa a lógica de gerenciamento de memória com as seguintes características:

1.  **Inicialização:** O simulador é configurado com:
    -   O tamanho da memória física (em número de quadros).
    -   O tamanho da memória virtual (em número de páginas).

2.  **Simulação de Acesso:** O programa processa uma sequência de acessos a páginas virtuais. Para cada acesso:
    -   Ele consulta a **Tabela de Páginas** para verificar se a página está na memória física (um *hit*).
    -   Se a página não estiver presente, ocorre uma **Falha de Página** (*page fault*).

3.  **Tratamento de Falha de Página:**
    -   O simulador procura por um quadro livre na memória física para carregar a nova página.
    -   Se a memória física estiver cheia, o algoritmo de substituição **FIFO (First-In, First-Out)** é acionado para escolher uma página a ser removida.
    -   A Tabela de Páginas é atualizada para refletir o novo estado da memória.

4.  **Saída:** Durante a execução, o simulador exibe o estado da memória física a cada passo e informa a ocorrência de *hits* e *page faults*. Ao final, ele apresenta o número total de falhas de página.

### Como Executar

Para rodar a simulação, basta executar o script Python em um terminal:

```bash
python simulador.py
```

Atualmente, os parâmetros da simulação (tamanhos de memória e sequência de acesso) estão definidos diretamente no código, na função `main()`.


## Casos de Teste para Validação do Simulador

Esta seção contém casos de testes projetada para validar a funcionalidade e a robustez do simulador de gerenciamento de memória. Cada teste foca em um aspecto específico do comportamento do algoritmo FIFO.

### Categoria 1: Testes de Funcionalidade Básica

---

#### Teste 1: Sequência Vazia
* **Objetivo:** Garantir que o programa lida com uma entrada vazia sem erros.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `10`
    * Sequência de Acesso: ``
* **Comportamento Esperado:** O programa deve iniciar e finalizar sem erros, resultando em 0 *Page Faults* e 0 *Hits*.

---

#### Teste 2: Sem Substituição
* **Objetivo:** Verificar o preenchimento inicial da memória quando a sequência de acesso é menor que a capacidade da memória física.
* **Parâmetros:**
    * Memória Física: `5`
    * Memória Virtual: `10`
    * Sequência de Acesso: `0 1 2 3`
* **Comportamento Esperado:** Devem ocorrer exatamente 4 *Page Faults*. Nenhuma substituição deve ser realizada.

---

#### Teste 3: Substituição Simples
* **Objetivo:** Confirmar a lógica básica do FIFO com uma única substituição.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `5`
    * Sequência de Acesso: `0 1 2 3`
* **Comportamento Esperado:** Devem ocorrer 4 *Page Faults*. Ao acessar a página `3`, a página `0` (a primeira a entrar) deve ser substituída.

### Categoria 2: Testes de Comportamento do Algoritmo

---

#### Teste 4: Alta Localidade de Referência
* **Objetivo:** Simular um programa que acessa repetidamente um pequeno conjunto de páginas, resultando em uma alta taxa de *hits* após o preenchimento inicial.
* **Parâmetros:**
    * Memória Física: `4`
    * Memória Virtual: `10`
    * Sequência de Acesso: `1 2 3 1 2 3 1 2 3 4 1 2 3 4`
* **Comportamento Esperado:** Após as falhas iniciais para carregar as páginas {1, 2, 3}, a maioria dos acessos subsequentes a elas devem ser *hits*.

---

#### Teste 5: Anomalia de Belady (Parte A)
* **Objetivo:** Estabelecer a linha de base de falhas com uma quantidade menor de memória física.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `5`
    * Sequência de Acesso: `0 1 2 3 0 1 4 0 1 2 3 4`
* **Comportamento Esperado:** O resultado final deve ser de **9 Page Faults**.

---

#### Teste 6: Anomalia de Belady (Parte B)
* **Objetivo:** Demonstrar que, com FIFO, aumentar a memória física pode, paradoxalmente, aumentar o número de falhas.
* **Parâmetros:**
    * Memória Física: `4`
    * Memória Virtual: `5`
    * Sequência de Acesso: `0 1 2 3 0 1 4 0 1 2 3 4`
* **Comportamento Esperado:** O número de *Page Faults* deve ser **10**, um valor maior que no Teste 5.

---

#### Teste 7: Pior Caso para o FIFO (Varredura Circular)
* **Objetivo:** Explorar o cenário de pior desempenho do FIFO, onde a página necessária é sempre a que acabou de ser removida.
* **Parâmetros:**
    * Memória Física: `4`
    * Memória Virtual: `10`
    * Sequência de Acesso: `0 1 2 3 4 0 1 2 3 4 0 1 2 3 4`
* **Comportamento Esperado:** A taxa de falhas de página será extremamente alta, com quase todos os acessos resultando em falha após o preenchimento inicial.

### Categoria 3: Testes de Casos Limítrofes (Edge Cases)

---

#### Teste 8: Memória com Apenas Um Quadro
* **Objetivo:** Testar o comportamento em uma condição de recurso extremamente limitado.
* **Parâmetros:**
    * Memória Física: `1`
    * Memória Virtual: `10`
    * Sequência de Acesso: `0 1 2 3 0 1`
* **Comportamento Esperado:** Cada acesso a uma página diferente da que está na memória resultará em um *Page Fault*.

---

#### Teste 9: Acessos Consecutivos à Mesma Página
* **Objetivo:** Garantir que acessos repetidos à mesma página resultem em *hits* após a primeira falha.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `10`
    * Sequência de Acesso: `5 5 5 5 5`
* **Comportamento Esperado:** O resultado deve ser exatamente 1 *Page Fault* e 4 *Hits*.

---

#### Teste 10: Acesso a Página Inválida
* **Objetivo:** Confirmar que o tratamento de erro para acessos fora do limite da memória virtual está funcionando.
* **Parâmetros:**
    * Memória Física: `3`
    * Memória Virtual: `5`
    * Sequência de Acesso: `0 1 2 99 3 4`
* **Comportamento Esperado:** O programa não deve quebrar. Ele deve exibir o aviso "AVISO: Acesso à página virtual inválida 99. Ignorando." e continuar a simulação normalmente.