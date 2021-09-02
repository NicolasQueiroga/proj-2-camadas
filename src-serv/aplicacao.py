#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from enlace import *
import timeit
import numpy as np
from PIL import Image
from io import BytesIO


#   python -m serial.tools.list_ports
serialName = "/dev/cu.usbmodem1412201"

def main():
    try:
        START = False
        READING = True
        FLAG = 0

        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()

        # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print('\n---> A comunicação foi aberta com sucesso!\n')
        
        while not START:
            byte = com1.getData(1)
            # print(byte) #DEBUG
            # print(byte[0]) #DEBUG
            if byte[0] == b'\xaa':
                print('---> Recebeu o AA\n')
                START = True
        

        comandos = []
        comando = b''

        print('---> Lendo o Pacote enviado\n')
        while READING:
            byte = com1.getData(1)
            # print(byte) #DEBUG
            if byte[0] != b'\xee':
                if FLAG == 0:
                    FLAG = int.from_bytes(byte[0], "big")
                else:
                    if FLAG == 1:
                        comando += byte[0]
                        comandos.append(comando)
                        comando = b''
                    else:
                        comando += byte[0]
                    FLAG -= 1
            else:
                print('---> Recebeu o EE\n')
                READING = False


        # print(len(comandos)) #DEBUG
        n_comandos = int(len(comandos)).to_bytes(1,'big')
        # print(n_comandos) #DEBUG
        # teste_envio = b'\x01' #DEBUG

        com1.sendData(n_comandos)

        # Encerra comunicação
        print("-----------------------------")
        print("---> Comunicação encerrada")
        print("-----------------------------")
        com1.disable()


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
