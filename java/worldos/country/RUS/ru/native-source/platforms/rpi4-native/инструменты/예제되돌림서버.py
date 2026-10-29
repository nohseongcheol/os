#!/usr/bin/env python3
"""русский 네트워크 예제용 узел TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class вывод_на_экран_Серверы:
    def __init__(자신,TCP_порт=0,UDP_порт=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class маркер_контакт_запрос(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);данные=bytearray()
                while b'\n' not in данные and len(данные)<=512:
                    блок_ЗНАЧЕН_652d4b53=자신.request.recv(512)
                    if not блок_ЗНАЧЕН_652d4b53:return
                    данные.extend(блок_ЗНАЧЕН_652d4b53)
                수신됨.append(('tcp',bytes(данные)));자신.request.sendall(данные)
        class датаграмма_маркер_запрос(socketserver.BaseRequestHandler):
            def handle(자신):
                данные,сокет_ЗНАЧЕН=자신.request;수신됨.append(('udp',данные));сокет_ЗНАЧЕН.sendto(данные,자신.client_address)
        자신.контакт_управление=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_порт),маркер_контакт_запрос)
        try:자신.датаграмма_управление=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_порт),датаграмма_маркер_запрос)
        except Exception:자신.контакт_управление.server_close();raise
        자신.контакт_управление.daemon_threads=자신.датаграмма_управление.daemon_threads=True
        자신.TCP_порт=자신.контакт_управление.server_address[1];자신.UDP_порт=자신.датаграмма_управление.server_address[1]

    def __enter__(자신):
        for сервер_ЗНАЧЕН in (자신.контакт_управление,자신.датаграмма_управление):
            фоноваяЗадача=threading.Thread(target=сервер_ЗНАЧЕН.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            фоноваяЗадача.start();자신.작업가닥들.append(фоноваяЗадача)
        return 자신

    def __exit__(자신,*аргумент_МАССИВ):
        for сервер_ЗНАЧЕН in (자신.контакт_управление,자신.датаграмма_управление):сервер_ЗНАЧЕН.shutdown();сервер_ЗНАЧЕН.server_close()
        for фоноваяЗадача in 자신.작업가닥들:фоноваяЗадача.join(timeout=1)


if __name__=='__main__':
    анализатор=argparse.ArgumentParser(description=__doc__)
    анализатор.add_argument('--tcp-port',type=int,default=9000);анализатор.add_argument('--udp-port',type=int,default=9001)
    аргумент_МАССИВ=анализатор.parse_args()
    with вывод_на_экран_Серверы(аргумент_МАССИВ.tcp_port,аргумент_МАССИВ.udp_port) as вывод_на_экран_сервер_ввод:
        print('узел TCP {}, UDP {} Подготовить. 게스트 АДРЕС: 10.0.2.2. Выход_программа: Ctrl+C'.format(вывод_на_экран_сервер_ввод.TCP_порт,вывод_на_экран_сервер_ввод.UDP_порт),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
