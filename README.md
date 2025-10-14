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
