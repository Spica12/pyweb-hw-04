import logging
import mimetypes
import socket
import urllib
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread

BASE_DIR = Path()
STORAGE_DIR = "storage"
LOG_FILE_NAME = "logs.txt"
STORAGE_FILE = "data.json"
BUFFER_SIZE = 1024
HTTP_HOST = "192.168.0.30"  # TODO Change to '0.0.0.0' before creating docker image
HTTP_PORT = 3000
SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 5000


class HWFramework(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"Starting function GET")

        route = urllib.parse.urlparse(self.path)
        logger.debug(f"path: {route.path}")

        match route.path:
            case "/":
                self.send_html("index.html")
            case "/message":
                self.send_html("message.html")
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                logger.debug(f"file: {file}")
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html("error.html", status_code=400)

        logger.info(f"Finished function GET")

    def do_POST(self):
        logger.info(f"Starting function POST")
        # logger.debug(f'Headers: {self.headers}')

        size = self.headers.get("Content-Length")
        logger.debug(f"Content-Length: {size}")

        data = self.rfile.read(int(size))
        logger.debug(f"Data: {data}")

        socket_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        socket_client.sendto(data, (SOCKET_HOST, SOCKET_PORT))
        socket_client.close()
        logger.debug("Send data to socket server")

        self.send_response(302)
        self.send_header(keyword="Location", value="/message")
        self.end_headers()

        logger.info(f"Finished function POST")

    def send_html(self, filename, status_code=200):
        logger.info(f"Start sending: {filename}")

        self.send_response(status_code)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        with open(filename, "rb") as file:
            self.wfile.write(file.read())

        logger.info(f"Finished sending: {filename}, status: {status_code}")

    def send_static(self, filename, status_code=200):
        logger.info(f"Start sending: {filename}")

        self.send_response(status_code)

        mime_types, *_ = mimetypes.guess_type(filename)

        if mime_types:
            self.send_header("Content-Type", mime_types)
            logger.debug(f"Content-Type: {mime_types}")
        else:
            self.send_header("Content-Type", "text/plain")
            logger.debug(f"Content-Type: text/plain")

        self.end_headers()

        with open(filename, "rb") as file:
            self.wfile.write(file.read())

        logger.info(f"Finished sending: {filename}, status: {status_code}")


def save_data_from_form(data):
    logger.info(f"Start saving data to storage")

    current_date = str(datetime.now())
    logger.debug(f"Current date: {current_date}")

    parse_data = urllib.parse.unquote_plus(data.decode())
    logger.debug(f"parse data: {parse_data}")

    storage_path = BASE_DIR / STORAGE_DIR / STORAGE_FILE
    try:
        parse_dict = {
            key: value for key, value in [el.split("=") for el in parse_data.split("&")]
        }
        logger.debug(f"parse dict: {parse_dict}")

        storage_dict = {}

        if storage_path.is_file():
            logger.debug(f"File {storage_path} exists")
            with open(storage_path, "r", encoding="utf-8") as file:
                storage_dict = json.load(file)
        else:
            logger.debug(f"File {storage_path} doesn't exist")

        storage_dict[current_date] = parse_dict

        with open(storage_path, "w", encoding="utf-8") as file:
            json.dump(storage_dict, file, ensure_ascii=False, indent=4)

    except ValueError as e:
        logger.error(e)
    except OSError as e:
        logger.error(e)

    logger.info(f"Data has saved to {storage_path}")


def run_http_server(host, port):
    address = (host, port)

    server = HTTPServer(address, HWFramework)
    logger.info(f"Created HTTP server: {address}")

    try:
        server.serve_forever()
        logger.info(f"Run HTTP server")
    except KeyboardInterrupt:
        logger.error(f"HTTP server has stopped by user")
    finally:
        server.close()
        logger.info(f"HTTP server closed")


def run_socket_server(host, port):
    address = (host, port)

    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind(address)
    logger.info(f"Run Socket server: {address}")

    try:
        while True:
            msg, address = server.recvfrom(BUFFER_SIZE)
            logger.debug(f"Received from: {address}: {msg}")
            save_data_from_form(msg)
    except KeyboardInterrupt:
        logger.error(f"Socket server has stopped by user")
    finally:
        server.close()
        logger.info(f"Socket server closed")


if __name__ == "__main__":
    logger = logging.getLogger("pylog")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(threadName)15s - %(funcName)20s(%(lineno)3d) - %(levelname)5s - %(message)s"
    )

    path_logs = BASE_DIR / LOG_FILE_NAME

    # TODO Щоб при кожному запуску файл з логами перезаписувався
    with open(path_logs, "w") as file:
        file.write("")

    fh = logging.FileHandler(filename=path_logs)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f'Start "PyWeb-homework-04')

    server = Thread(
        name="HTTP server", target=run_http_server, args=(HTTP_HOST, HTTP_PORT)
    )
    server.start()

    server_socket = Thread(
        name="Socket server", target=run_socket_server, args=(SOCKET_HOST, SOCKET_PORT)
    )
    server_socket.start()
