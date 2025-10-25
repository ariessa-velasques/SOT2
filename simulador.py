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
        
        # Contadores de estatísticas.
        self.falhas_de_pagina = 0
        self.hits = 0 

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
            self.hits += 1
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
        # Exibe o estado bruto da memória física
        print("   Estado da Memória Física (Quadros):", self.memoria_fisica)
        # Exibe o estado da estrutura de controle do algoritmo (FIFO)
        print("   Estado da Fila FIFO (Páginas):   ", list(self.fila_fifo))
        # Exibe o mapeamento explícito (Requisito do enunciado)
        print("   Mapeamento (Página Virtual -> Quadro Físico):")
        
        # Cria um dicionário com apenas as páginas que estão na memória
        mapeamento_ativo = {}
        for i, info in enumerate(self.tabela_paginas):
            # info[0] é o bit de presença, info[1] é o quadro
            if info[0] == 1:
                mapeamento_ativo[i] = info[1]

        if not mapeamento_ativo:
            print("     (Nenhuma página na memória física)")
        else:
            # Ordena o mapeamento pelo número do quadro (índice 1 do valor do dict)
            # Isso torna a leitura mais limpa e alinhada com a lista da memória física
            itens_ordenados = sorted(mapeamento_ativo.items(), key=lambda item: item[1])
            for pagina, quadro in itens_ordenados:
                print(f"      Página {pagina} -> Quadro {quadro}")
        print() 

    def executar_simulacao(self, sequencia_acesso):
        """
        Executa a simulação com uma lista de acessos a páginas virtuais.
        """
        print("--- INÍCIO DA SIMULAÇÃO ---")
        self.imprimir_estado_memoria()
        
        for pagina in sequencia_acesso:
            self.acessar_endereco_virtual(pagina)
            
        print("--- FIM DA SIMULAÇÃO ---")
        
        total_acessos = len(sequencia_acesso)
        if total_acessos > 0:
            taxa_falhas = (self.falhas_de_pagina / total_acessos) * 100
            taxa_hits = (self.hits / total_acessos) * 100
        else:
            taxa_falhas = taxa_hits = 0

        print(f"Total de Acessos: {total_acessos}")
        print(f"Total de Page Faults: {self.falhas_de_pagina} ({taxa_falhas:.2f}%)")
        print(f"Total de Hits: {self.hits} ({taxa_hits:.2f}%)")


# --- FUNÇÃO PRINCIPAL PARA EXECUÇÃO ---
def main():
    """
    Função principal que configura e executa o simulador de forma interativa.
    """
    print("--- Simulador de Gerenciamento de Memória com Paginação ---")
    print("Por favor, forneça os dados para a simulação.\n")

    try:
        # Solicita e valida as entradas do usuário
        quadros_memoria_fisica = int(input("1. Digite o tamanho da Memória Física (em nº de quadros): "))
        paginas_memoria_virtual = int(input("2. Digite o tamanho da Memória Virtual (em nº de páginas): "))
        
        entrada_sequencia = input("3. Digite a sequência de acesso (páginas separadas por espaço): ")
        
        # Converte a string de entrada em uma lista de números inteiros
        sequencia_acesso = [int(p) for p in entrada_sequencia.split()]

    except ValueError:
        print("\n[ERRO] Entrada inválida. Por favor, certifique-se de digitar apenas números inteiros.")
        return # Encerra o programa se a entrada for inválida
    
    print("-" * 50)

    # Cria uma instância do simulador com os dados fornecidos pelo usuário
    simulador = MemoryManagementSimulator(
        quadros_fisicos=quadros_memoria_fisica,
        paginas_virtuais=paginas_memoria_virtual
    )

    # Executa a simulação com a sequência de acesso
    simulador.executar_simulacao(sequencia_acesso=sequencia_acesso)

# Garante que a função main() será executada quando o script for rodado
if __name__ == "__main__":
    main()
