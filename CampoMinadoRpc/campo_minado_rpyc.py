from random import randint

import rpyc
from rpyc.utils.server import ThreadedServer

class CampoMinadoRpyc(rpyc.Service):

    def __init__(self, linha = 5, coluna = 5):
        self.__linha = int(linha)
        self.__coluna = int(coluna)
        self.jogadas_restantes = self.__calcular_total_jogadas(linha, coluna)
        self.__tabuleiro = self.__inicializar_tabuleiro(linha, coluna)
        self.__coordenadas_bombas = self.__distribuir_bombas(linha,coluna)
        self.__coordenada_valida = True
        self.__jogada_segura = True
        self.__game_over = False

    def exposed_get_tabuleiro(self):
        return self.__tabuleiro

    def exposed_get_jogada_segura(self):
        return self.__jogada_segura
    
    def exposed_get_game_over(self):
        return self.__game_over
    
    def exposed_coordenada_valida(self):
        return self.__coordenada_valida

    def exposed_jogadas_restantes(self):
        return self.jogadas_restantes

    def exposed_jogada(self, linha, coluna):
        linha = int(linha)
        coluna = int(coluna)

        if not self.__validar_coordenadas(linha, coluna):
            self.__coordenada_valida = False

        if  (linha, coluna) in self.__coordenadas_bombas:
            self.__game_over = True

        self.__tabuleiro[linha][coluna] = str(self.__conta_bombas_vizinhos(linha, coluna))
        self.jogadas_restantes -=1
        self.__jogada_segura = True

    def exposed_imprimir_tabuleiro(self):
        for posicao in self.__tabuleiro:
            print(str(posicao))
    
    def jogo_incompleto(self):
        return False

    def __inicializar_tabuleiro(self, linha, coluna):
        return [[str('X') for x in range(coluna)] for j in range(linha)]

    def __distribuir_bombas(self, linha, coluna):
        coordenadas_bombas = [(randint(0, linha - 1), randint(0, coluna - 1)) for x in range(self.__total_bombas())]
        print(coordenadas_bombas)
        return coordenadas_bombas

    def __total_bombas(self):
        return int((self.__linha*self.__coluna)/3)
    
    def __calcular_total_jogadas(self,linha, coluna):
        return (linha*coluna) - self.__total_bombas()

    def __validar_coordenadas(self, linha, coluna):
        if linha in range(0, self.__linha) and coluna in range(0, self.__coluna):
            return True
        return False
    
    def __coordenada_e_bomba(self, coordenada):
        return coordenada in self.__coordenadas_bombas

    def __conta_bombas_vizinhos(self, linha, coluna):
        return len([(linha + x, coluna + y) for x in (-1,0,1) for y in (-1,0,1) if self.__coordenada_e_bomba((linha + x, coluna + y))])

def server():
    thread = ThreadedServer(CampoMinadoRpyc, port=8080)
    thread.start()