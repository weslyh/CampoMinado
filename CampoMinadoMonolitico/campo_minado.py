import random

# 0 = Espaço em Branco
# -1 = Bomba

class tabuleiroCell(object):
    valor = 0
    selecionado = False
    mina = False

    def __init__(self):
        self.selecionado = False

    def __str__(self):
        return str(tabuleiroCell.valor)

    def isMina(self):
        if tabuleiroCell.valor == -1:
            return True
        return False


class tabuleiroClass(object):
    def __init__(self, m_tabuleiroSize, m_numMinas):
        self.tabuleiro = [[tabuleiroCell() for i in range(m_tabuleiroSize)] for j in range(m_tabuleiroSize)]
        self.tabuleiroSize = m_tabuleiroSize
        self.numMinas = m_numMinas
        self.celulasSelecionadas = m_tabuleiroSize * m_tabuleiroSize - m_numMinas
        i = 0
        while i < m_numMinas:
            x = random.randint(0, self.tabuleiroSize-1)
            y = random.randint(0, self.tabuleiroSize-1)
            if not self.tabuleiro[x][y].mina:
                self.addMina(x, y)
                i += 1
            else:
                i -= 1

    def __str__(self):
        returnString = " "
        linha = "\n---"

        for i in range(0, self.tabuleiroSize):
            returnString += " | " + str(i)
            linha += "----"
        linha += "\n"

        returnString += linha
        for y in range(0, self.tabuleiroSize):
            returnString += str(y)
            for x in range(0, self.tabuleiroSize):
                if self.tabuleiro[x][y].mina and self.tabuleiro[x][y].selecionado:
                    returnString += " |" + str(self.tabuleiro[x][y].valor)
                elif self.tabuleiro[x][y].selecionado:
                    returnString += " | " + str(self.tabuleiro[x][y].valor)
                else:
                    returnString += " |  "
            returnString += " |"
            returnString += linha
        return returnString

    def addMina(self, x, y):
        self.tabuleiro[x][y].valor = -1
        self.tabuleiro[x][y].mina = True
        for i in range(x-1, x+2):
            if i >= 0 and i < self.tabuleiroSize:
                if y-1 >= 0 and not self.tabuleiro[i][y-1].mina:
                    self.tabuleiro[i][y-1].valor += 1
                if y+1 < self.tabuleiroSize and not self.tabuleiro[i][y+1].mina:
                    self.tabuleiro[i][y+1].valor += 1
        if x-1 >= 0 and not self.tabuleiro[x-1][y].mina:
            self.tabuleiro[x-1][y].valor += 1
        if x+1 < self.tabuleiroSize and not self.tabuleiro[x+1][y].mina:
            self.tabuleiro[x+1][y].valor += 1

    def fazerJogada(self, x, y):
        self.tabuleiro[x][y].selecionado = True
        self.celulasSelecionadas -= 1
        if self.tabuleiro[x][y].valor == -1:
            return False
        if self.tabuleiro[x][y].valor == 0:
            for i in range(x-1, x+2):
                if i >= 0 and i < self.tabuleiroSize:
                    if y-1 >= 0 and not self.tabuleiro[i][y-1].selecionado:
                        self.fazerJogada(i, y-1)
                    if y+1 < self.tabuleiroSize and not self.tabuleiro[i][y+1].selecionado:
                        self.fazerJogada(i, y+1)
            if x-1 >= 0 and not self.tabuleiro[x-1][y].selecionado:
                self.fazerJogada(x-1, y)
            if x+1 < self.tabuleiroSize and not self.tabuleiro[x+1][y].selecionado:
                self.fazerJogada(x+1, y)
            return True
        else:
            return True

    def selecionarMina(self, x, y):
        return self.tabuleiro[x][y].valor == -1

    def isVencedor(self):
        return self.celulasSelecionadas == 0

def jogo():
    tamanhoTabuleiro = int(input("Escolha o tamanho do tabuleiro: "))
    numMinas = int(input("Escolha a quantidade de bombas: "))
    gameOver = False
    vencedor = False
    Tabuleiro = tabuleiroClass(tamanhoTabuleiro, numMinas)
    while not gameOver:
        print(Tabuleiro)
        print("Faça sua jogada:")
        x = int(input("x: "))
        y = int(input("y: "))
        Tabuleiro.fazerJogada(x, y)
        gameOver = Tabuleiro.selecionarMina(x, y)
        if Tabuleiro.isVencedor() and gameOver == False:
            gameOver = True
            vencedor = True

    print(Tabuleiro)
    if vencedor:
        print("Parabéns, você venceu !")
    else:
        print("BOOOOM, Game Over !")

jogo()
