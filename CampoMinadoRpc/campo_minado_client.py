import time
import rpyc
import sys

def display_campo_minado(self):
    for display in self.display:
        print(display)

def start_game():
    config = {'allow_public_attrs': True}
    cm = rpyc.connect('localhost', 8080, config=config)

    while True:
        tabuleiro = cm.root.get_tabuleiro()
        print(tabuleiro)

        print('\nFaça sua jogada: \n')
        linha = input('Escolha a linha:')
        coluna = input('Escolha a coluna:')
        cm.root.jogada(linha=int(linha),coluna=int(coluna))

        if cm.root.get_coordenada_valida():
            if cm.root.get_jogada_segura():
                cm.root.get_tabuleiro()
            elif cm.root.get_game_over():
                print("Você acertou uma bomba ! \n")
                cm.root.get_tabuleiro()
        else:
            print("Jogada inválida !")        
        
def client():
    while True:
        print('###### Menu ######:\n')
        print('###### 1 - INICIAR JOGO ######\n')
        print('###### 2 - Sair ######')
        opcao = input('O que você me conta ? 1 ou 2 ? \n ')
        if opcao == '1':
            start_game()
            continue
        elif opcao == '2':
            print('BYE')
            sys.exit(0)
            break
        else:
            print('Entrada inválida')
            continue
