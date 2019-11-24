import zmq
from campo_minado_negocio import CampoMinado
from ast import literal_eval

PORT = "5560"

context = zmq.Context()
conn = context.socket(zmq.REP)
conn.connect("tcp://localhost:%s" % PORT)

print("Conectado: ")

objeto = CampoMinado

def novoJogo(mensagem,objeto):
    linMax = mensagem['linMax']
    colMax = mensagem['colMax']
    print(mensagem)
    objeto = CampoMinado(linMax,colMax)
    print(objeto)
    totBombas = objeto.total_bombas()
    if(linMax != 0):
        objetoConS = {'totalBombas':totBombas}
        print(objetoConS)
    else:
        linhaColuna = objeto.linhaColuna()
        objetoConS = {'totalBombas':totBombas,'linha':linhaColuna['linha'],'coluna':linhaColuna['coluna']}
    
    objeto.salvarJogo()
    return objetoConS

def jogada(mensagem,objeto):
    lin = mensagem['linha']
    col = mensagem['coluna']
    objetoConS = objeto.jogada(lin,col)
    return objetoConS

while True:
    objetoConR = conn.recv().decode()

    mensagem = literal_eval(objetoConR)
    print(mensagem)

    if(mensagem['tipo'] == 'novoJogo'):
        print("Criando novo Jogo")
        resposta = novoJogo(mensagem,objeto)    
        conn.send(str(resposta).encode())

    if(mensagem['tipo'] == 'retorna_tabuleiro'):
        print("Impressao do Tabuleiro")
        objeto = CampoMinado()
        tabuleiro = objeto.retornaTabuleiro()
        print(tabuleiro)
        resposta = str(tabuleiro)
        conn.send(resposta.encode())

    if(mensagem['tipo'] == 'jogada'):
        objeto = CampoMinado(0,0)
        resposta = jogada(mensagem,objeto)
        conn.send(str(resposta).encode())

    if(mensagem['tipo'] == 'matriz_bomba'):
        objetoConS = objeto.matriz_bomba(mensagem['board'])
        conn.send(str(objetoConS).encode())