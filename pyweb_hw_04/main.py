import logging

from pathlib import Path
from threading import Thread


BASE_DIR = Path()
LOG_FILE_NAME = 'logs.txt'
BUFFER_SIZE = 1024
HTTP_HOST = 'localhost'     # TODO Change to '0.0.0.0' before creating docker image
HTTP_PORT = 3000
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 5000

def run_http_server(port, host):
    logger.info(f'Run HTTP server: ({port}, {host})')
    pass


def run_socket_server(port, host):
    logger.info(f'Run Socket server: ({port}, {host})')
    pass    


if __name__ == '__main__':
    logger = logging.getLogger('pylog')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)5s - %(threadName)15s - %(funcName)20s(%(lineno)d) - %(message)s')

    path_logs = BASE_DIR / LOG_FILE_NAME

    # TODO Щоб при кожному запуску файл з логами перезаписувався
    with open(path_logs, 'w') as file:
        file.write('')

    fh = logging.FileHandler(filename=path_logs)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f'Start "PyWeb-homework-04')

    server = Thread(name='HTTP server', target=run_http_server, args=(HTTP_PORT, HTTP_HOST))
    server.start()
    
    server_socket = Thread(name='Socket server', target=run_socket_server, args=(SOCKET_PORT, SOCKET_HOST))
    server_socket.start()








