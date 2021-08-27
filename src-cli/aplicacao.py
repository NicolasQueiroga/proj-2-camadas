#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2020
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from sys import byteorder
from enlace import *
import timeit
import random
import numpy as np
from PIL import Image
from io import BytesIO


# Port do arduino
serialName = "/dev/ttyACM0"

# Lista de comandos existentes
comandos = [0x00FF.to_bytes(2, byteorder='big'), 0x00.to_bytes(1, byteorder='big'), 0x0F.to_bytes(1, byteorder='big'), 0xF0.to_bytes(1, byteorder='big'), 0xFF00.to_bytes(2, byteorder='big'), 0xFF.to_bytes(1, byteorder='big')]

# Lista inicializada para envio
global send
send = [0xAA.to_bytes(1, byteorder='big')]


def main():
    '''
        Função que realiza a comunicação entre os arduinos
    '''
    try:
        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()
        print('\n---> A comunicação foi aberta com sucesso!\n')

        # Inicia o timer
        t1 = timeit.default_timer()

        # Montando lista aleatória de 10 a 30 comandos do formato [size, cmd, size, cmd, ...]
        n_commands = random.randint(10, 30)
        for _ in np.arange(n_commands):
            i = random.randint(0, 5)
            cmd = comandos[i]
            n_cmd_byte = len(cmd).to_bytes(1, byteorder='big')
            send.append(n_cmd_byte)
            send.append(cmd)
        send.append(0xEE.to_bytes(1, byteorder='big'))

        print(f'---> Sequência: \n{send} (lista de bytes)')
        print(f'---> Número de comandos: {n_commands}\n')

        # 
        txBuffer = (b''.join(send))
        print(f'---> txBuffer: {txBuffer}')
        
        txBuffer_size = int(len(txBuffer))
        # txBuffer_size_hex = bytes([(txBuffer_size)])
        txBuffer_size_hex = bytes([(txBuffer_size)])

        print(f'---> txBuffer size: {txBuffer_size}')
        print(f"---> txBuffer size hex: {txBuffer_size_hex}")

        # Iniciando a transmição de dados
        com1.sendData(txBuffer)

        print('\n---> A recepção vai começar!')

        print('DEBUG 1')

        # Recebendo o byte que representa o tamanho do array enviado
        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(1)
        print('DEBUG 2')
        print("\nRecebido:\n {}\n" .format(rxBuffer))
        recebidos = int.from_bytes(rxBuffer, 'big')
        print(f'Tamanho da sequência enviada = Tamanho da sequência recebida? {recebidos == n_commands}')

        # Encerra comunicação
        print("-----------------------------")
        print("---> Comunicação encerrada")
        com1.disable()

        t2 = timeit.default_timer()
        print(f'---> process took {t2 - t1} seconds')
        print("-----------------------------")

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
