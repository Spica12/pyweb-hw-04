import logging

from pathlib import Path


BASE_DIR = Path()
LOG_FILE_NAME = 'logs.txt'


def run_http_server():
    logger.debug('Run HTTP server')
    pass


def run_socket_server():
    logger.debug('Run Socket server')
    pass    


if __name__ == '__main__':
    logger = logging.getLogger('pylog')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)5s - %(threadName)s - %(funcName)20s(%(lineno)d) - %(message)s')

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

    logger.debug(f'Start "PyWeb-homework-04')

    run_http_server()
    run_socket_server()






