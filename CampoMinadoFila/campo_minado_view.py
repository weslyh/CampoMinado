import zmq
import os
import sys
from ast import literal_eval
import platform

board = []

boardbomba = []

def limpaTela():
    so = platform.system()
    if(so != 'Windows'):
        unused_variable = os.system("clear")
    else:
        unused_variable = os.system("cls")

def imprimir_tabuleiro(board):
        for posicao in board:
            print(str(posicao))

def principal(conexao,linMax,colMax):
    objetoConS = {'tipo':'novoJogo', 'linMax': linMax,'colMax':colMax}
    conexao.send(str(objetoConS).encode())
    objetoConR  = conexao.recv(1024).decode()
    objeto = literal_eval(objetoConR)

    """ Total de Jogadas """
    jogadas = 0

    perdeu = False

    qtd_bombas = objeto['totalBombas']

    if(linMax == 0 and colMax == 0):
        linMax = objeto['linha']
        colMax = objeto['coluna']

    msg = 0

    while not(perdeu):
        limpaTela()
        print("Digite 0 na linha e 0 na coluna para Salvar e Sair")

        objetoConS = {'tipo':'retorna_tabuleiro'}
        conexao.send(str(objetoConS).encode())
        objetoConR  = conexao.recv(1024).decode()
        board = literal_eval(objetoConR)
        imprimir_tabuleiro(board)

        lin = int(input("Digite a linha: "))
        col = int(input("Digite a coluna: "))

        objetoConS = {'tipo':'jogada','linha':lin,'coluna':col}
        conexao.send(str(objetoConS).encode())
        objetoConR  = conexao.recv(1024).decode()
        perdeu = literal_eval(objetoConR)
        jogadas = jogadas + 1
        if(perdeu == False):
            if ((((linMax)*(colMax))-jogadas) == int(qtd_bombas)):
                print("\nPARABENS!! VOCE VENCEU!!!")
                perdeu = True
        elif(perdeu == 2):
            print("Jogo Salvo!!!\n")
            sys.exit(0)
        else:
            objetoConS = {'tipo':'matriz_bomba','board':board}
            conexao.send(str(objetoConS).encode())
            objetoConR  = conexao.recv(1024).decode()
            boardbomba = literal_eval(objetoConR)
            imprimir_tabuleiro(boardbomba)
            print("Fim de jogo !!")

    flag = str(input("Jogar de novo S/N?"))
    if(flag == 's' or flag == 'S'):
        board = []
        return True
    else:
        return False

def novoJogo(conexao):
    jogar = True

    while(jogar):
        limpaTela()
        linMax = int(input("Digite o total de linhas: "))
        colMax = int(input("Digite o total de colunas: "))
        jogar = principal(conexao,linMax,colMax)
    conexao.close()

def carregar_Jogo(conexao):
    retorno = principal(conexao,0,0)
    if(retorno == True):
        novoJogo(conexao)
    else:
        pass
    conexao.close()

def Menu():

    PORT = "5559"
    context = zmq.Context()
    conexao = context.socket(zmq.REQ)
    conexao.connect("tcp://localhost:%s" % PORT)

    listaMenu = ['Novo Jogo', 'Continuar','Sair']

    limpaTela()
    print(" CAMPO MINADO ","\n\n")
    print(" MENU ","\n")
    for i, v in enumerate(listaMenu):
        print(i+1, v,"\n\n")

    opcao = input("Escolha uma opcao: ")
    if(opcao == '1'):
        novoJogo(conexao)
    elif(opcao == '2'):
        carregar_Jogo(conexao)
    else:
        sys.exit(0)

Menu()