# Importa a classe 'deque' para usar como uma fila eficiente para o algoritmo FIFO
from collections import deque

class MemoryManagementSimulator:
    """
    Classe que encapsula a lógica do simulador de gerenciamento de memória.
    """
    def __init__(self, quadros_fisicos, paginas_virtuais):
        """
        Inicializa o simulador com os tamanhos de memória definidos.
        """
        if not (isinstance(quadros_fisicos, int) and quadros_fisicos > 0 and
                isinstance(paginas_virtuais, int) and paginas_virtuais > 0):
            raise ValueError("Os tamanhos das memórias devem ser números inteiros positivos.")

        self.numero_quadros_fisicos = quadros_fisicos
        self.numero_paginas_virtuais = paginas_virtuais
        
        # Memória física: -1 representa um quadro livre.
        self.memoria_fisica = [-1] * self.numero_quadros_fisicos
        
        # Tabela de páginas: mapeia [bit_de_presença, número_do_quadro_físico]
        self.tabela_paginas = [[0, -1] for _ in range(self.numero_paginas_virtuais)]
        
        # Fila para o algoritmo de substituição FIFO.
        self.fila_fifo = deque()
        
        # Contador de falhas de página.
        self.falhas_de_pagina = 0

    def acessar_endereco_virtual(self, pagina_virtual):
        """
        Simula o acesso a um endereço de memória virtual.
        """
        if not (0 <= pagina_virtual < self.numero_paginas_virtuais):
            print(f"--- AVISO: Acesso à página virtual inválida {pagina_virtual}. Ignorando. ---")
            return

        print(f"Acessando página virtual: {pagina_virtual}")

        # Se o bit de presença for 1, a página está na memória (hit).
        if self.tabela_paginas[pagina_virtual][0] == 1:
            print(f"  -> Hit! Página {pagina_virtual} já está na memória física no quadro {self.tabela_paginas[pagina_virtual][1]}.\n")
        else:
            # Caso contrário, ocorre uma falha de página (page fault).
            self.falhas_de_pagina += 1
            print(f"  -> Page Fault! Página {pagina_virtual} não está na memória física.")
            self.tratar_falha_de_pagina(pagina_virtual)
        
        self.imprimir_estado_memoria()


    def tratar_falha_de_pagina(self, nova_pagina):
        """
        Trata uma falha de página, carregando a nova página para a memória física.
        Utiliza o algoritmo FIFO se a memória estiver cheia.
        """
        try:
            # Tenta encontrar um quadro livre na memória física.
            indice_quadro_livre = self.memoria_fisica.index(-1)
            
            print(f"  -> Carregando página {nova_pagina} para o quadro físico livre {indice_quadro_livre}.")
            
            self.memoria_fisica[indice_quadro_livre] = nova_pagina
            self.fila_fifo.append(nova_pagina)
            
            # Atualiza a tabela de páginas para a nova página.
            self.tabela_paginas[nova_pagina][0] = 1
            self.tabela_paginas[nova_pagina][1] = indice_quadro_livre
            
        except ValueError:
            # Se não há quadros livres, aplica o algoritmo de substituição FIFO.
            pagina_a_ser_substituida = self.fila_fifo.popleft()
            
            print(f"  -> Memória física cheia. Substituindo a página {pagina_a_ser_substituida} (FIFO).")
            
            indice_quadro_substituido = self.tabela_paginas[pagina_a_ser_substituida][1]
            
            print(f"  -> Carregando página {nova_pagina} para o quadro físico {indice_quadro_substituido}.")

            # Coloca a nova página no quadro da página antiga.
            self.memoria_fisica[indice_quadro_substituido] = nova_pagina
            self.fila_fifo.append(nova_pagina)
            
            # Invalida a entrada da página antiga na tabela de páginas.
            self.tabela_paginas[pagina_a_ser_substituida][0] = 0
            self.tabela_paginas[pagina_a_ser_substituida][1] = -1
            
            # Atualiza a tabela de páginas para a nova página.
            self.tabela_paginas[nova_pagina][0] = 1
            self.tabela_paginas[nova_pagina][1] = indice_quadro_substituido

    def imprimir_estado_memoria(self):
        """
        Exibe o estado atual da memória física e da fila FIFO.
        """
        print("   Estado atual da Memória Física (Quadros):", self.memoria_fisica)
        print("   Estado atual da Fila FIFO (Páginas):   ", list(self.fila_fifo), "\n")


    def executar_simulacao(self, sequencia_acesso):
        """
        Executa a simulação com uma lista de acessos a páginas virtuais.
        """
        print("--- INÍCIO DA SIMULAÇÃO ---")
        self.imprimir_estado_memoria()
        
        for pagina in sequencia_acesso:
            self.acessar_endereco_virtual(pagina)
            
        print("--- FIM DA SIMULAÇÃO ---")
        print(f"Total de Page Faults: {self.falhas_de_pagina}")


# --- FUNÇÃO PRINCIPAL PARA EXECUÇÃO ---
def main():
    """
    Função principal que configura e executa o simulador.
    """
    # --- ENTRADAS DA SIMULAÇÃO (Valores fixos para teste) ---
    quadros_memoria_fisica = 3
    paginas_memoria_virtual = 10
    sequencia_acesso = [0, 1, 2, 3, 0, 4, 1, 5, 2, 6, 3, 7, 4, 8, 5, 9]

    # Cria uma instância do simulador
    simulador = MemoryManagementSimulator(
        quadros_fisicos=quadros_memoria_fisica,
        paginas_virtuais=paginas_memoria_virtual
    )

    # Executa a simulação com a sequência de acesso
    simulador.executar_simulacao(sequencia_acesso=sequencia_acesso)

    # --- PRÓXIMOS PASSOS ---
    # 1. Tornar as entradas interativas: Permitir que o usuário digite os tamanhos das memórias
    #    e a sequência de acesso ao invés de usar valores fixos.
    # 2. Criar mais cenários de teste: Adicionar outras listas de `sequencia_acesso` para
    #    validar o comportamento do simulador em diferentes condições.
    # 3. Escrever o relatório e a documentação final do trabalho.

# Garante que a função main() será executada quando o script for rodado
if __name__ == "__main__":
    main()