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
import random
import numpy as np


# Port do arduino
serialName = "/dev/ttyACM0"

# Lista de comandos existentes
comandos = [0x00FF.to_bytes(2, byteorder='big'), 0x00.to_bytes(1, byteorder='big'), 0x0F.to_bytes(
    1, byteorder='big'), 0xF0.to_bytes(1, byteorder='big'), 0xFF00.to_bytes(2, byteorder='big'), 0xFF.to_bytes(1, byteorder='big')]

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
        print('---> A comunicação foi aberta com sucesso!\n')

        # Inicia o timer
        t1 = timeit.default_timer()

        # Montando lista aleatória de 10 a 30 comandos do formato [start, cmd, size, cmd, ..., end]
        n_commands = random.randint(10, 30)
        for _ in np.arange(n_commands):
            i = random.randint(0, 5)
            cmd = comandos[i]
            n_cmd_byte = len(cmd).to_bytes(1, byteorder='big')
            send.append(n_cmd_byte)
            send.append(cmd)
        send.append(0xEE.to_bytes(1, byteorder='big'))

        print(f'---> Sequência:  {send} (lista de bytes)')
        print(f'---> Número de comandos: {n_commands}')

        # Iniciando a transmição de dados
        txBuffer = (b''.join(send))
        com1.sendData(txBuffer)

        print('\n---> A recepção vai começar!')

        # Recebendo o byte que representa o tamanho do array enviado
        rxBuffer, _ = com1.getData(1)
        print("\n---> Recebido: {}\n" .format(rxBuffer))
        recebidos = int.from_bytes(rxBuffer, 'big')
        print(
            f'Tamanho da sequência enviada = Tamanho da sequência recebida? {recebidos == n_commands}')

        # Encerra comunicação
        print("-----------------------------")
        print("---> Comunicação encerrada")
        com1.disable()

        print(f'---> process took {(timeit.default_timer() - t1):.8f} seconds')
        print("-----------------------------")

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
