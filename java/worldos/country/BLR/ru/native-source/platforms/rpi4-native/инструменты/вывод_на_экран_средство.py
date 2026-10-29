"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class вывод_на_экран_средство:
    def __enter__(자신):
        자신.контакт_управление = socket.socket(); 자신.контакт_управление.bind(('127.0.0.1', 0)); 자신.контакт_управление.listen(1)
        자신.датаграмма_управление = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 자신.датаграмма_управление.bind(('127.0.0.1', 0))
        자신.контакт_управление.settimeout(30); 자신.датаграмма_управление.settimeout(30)
        자신.TCP_порт = 자신.контакт_управление.getsockname()[1]; 자신.UDP_порт = 자신.датаграмма_управление.getsockname()[1]
        자신.오류들 = []; 자신.수신됨 = {}
        def контакт_управление():
            try:
                контакт_e05f319b, _ = 자신.контакт_управление.accept()
                with контакт_e05f319b:
                    контакт_e05f319b.settimeout(5); данные = bytearray()
                    while b'\n' not in данные:
                        блок_ЗНАЧЕН_652d4b53 = контакт_e05f319b.recv(512)
                        if not блок_ЗНАЧЕН_652d4b53: raise RuntimeError('TCP EOF before request')
                        данные.extend(блок_ЗНАЧЕН_652d4b53)
                    자신.수신됨['tcp'] = bytes(данные); контакт_e05f319b.sendall(данные)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        def датаграмма_управление():
            try:
                данные, одноранговый_ЗНАЧЕН = 자신.датаграмма_управление.recvfrom(512); 자신.수신됨['udp'] = данные; 자신.датаграмма_управление.sendto(данные, одноранговый_ЗНАЧЕН)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        자신.작업가닥들 = [threading.Thread(target=файл_ввод, daemon=True) for файл_ввод in (контакт_управление, датаграмма_управление)]
        for Терминал_ввод in 자신.작업가닥들: Терминал_ввод.start()
        return 자신

    def __exit__(자신, *аргумент_МАССИВ):
        자신.контакт_управление.close(); 자신.датаграмма_управление.close()
        for Терминал_ввод in 자신.작업가닥들: Терминал_ввод.join(timeout=1)
