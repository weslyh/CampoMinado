import sys
from campo_minado_rpyc import server
from campo_minado_client import testConection

print("Você quer executar:")
print("1 para servidor")
print("2 para cliente")

def iniciar_server():
    opcao = input("Opção:")

    try:
        if int(opcao) == 1:
            print("Servidor ativado:\n")
            server()
        elif int(opcao) == 2:
            print("Cliente ativado:\n")
            testConection()
    except:
        for val in sys.exc_info():
            print(val)

    input()