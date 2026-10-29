#!/usr/bin/env python3
"""українська 네트워크 예제용 хост TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class відлуння_Сервери:
    def __init__(자신,протокол_керування_передаванням_порт=0,протокол_користувацьких_дейтаграм_порт=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class маркер_зв_язок_запит(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);дані=bytearray()
                while b'\n' not in дані and len(дані)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    дані.extend(조각)
                수신됨.append(('tcp',bytes(дані)));자신.request.sendall(дані)
        class дейтаграма_маркер_запит(socketserver.BaseRequestHandler):
            def handle(자신):
                дані,сокет_значення=자신.request;수신됨.append(('udp',дані));сокет_значення.sendto(дані,자신.client_address)
        자신.зв_язок_керування=socketserver.ThreadingTCPServer(('127.0.0.1',протокол_керування_передаванням_порт),маркер_зв_язок_запит)
        try:자신.дейтаграма_керування=socketserver.ThreadingUDPServer(('127.0.0.1',протокол_користувацьких_дейтаграм_порт),дейтаграма_маркер_запит)
        except Exception:자신.зв_язок_керування.server_close();raise
        자신.зв_язок_керування.daemon_threads=자신.дейтаграма_керування.daemon_threads=True
        자신.протокол_керування_передаванням_порт=자신.зв_язок_керування.server_address[1];자신.протокол_користувацьких_дейтаграм_порт=자신.дейтаграма_керування.server_address[1]

    def __enter__(자신):
        for сервер_значення in (자신.зв_язок_керування,자신.дейтаграма_керування):
            фоноваЗадача=threading.Thread(target=сервер_значення.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            фоноваЗадача.start();자신.작업가닥들.append(фоноваЗадача)
        return 자신

    def __exit__(자신,*аргумент_масив):
        for сервер_значення in (자신.зв_язок_керування,자신.дейтаграма_керування):сервер_значення.shutdown();сервер_значення.server_close()
        for фоноваЗадача in 자신.작업가닥들:фоноваЗадача.join(timeout=1)


if __name__=='__main__':
    аналізатор=argparse.ArgumentParser(description=__doc__)
    аналізатор.add_argument('--tcp-port',type=int,default=9000);аналізатор.add_argument('--udp-port',type=int,default=9001)
    аргумент_масив=аналізатор.parse_args()
    with відлуння_Сервери(аргумент_масив.tcp_port,аргумент_масив.udp_port) as відлуння_сервер_запис:
        print('хост TCP {}, UDP {} Готувати. 게스트 Адреса: 10.0.2.2. Вийти_програма: Ctrl+C'.format(відлуння_сервер_запис.протокол_керування_передаванням_порт,відлуння_сервер_запис.протокол_користувацьких_дейтаграм_порт),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
