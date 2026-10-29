"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class 되돌림시험서버:
    def __enter__(자신):
        자신.conexión_control = socket.socket(); 자신.conexión_control.bind(('127.0.0.1', 0)); 자신.conexión_control.listen(1)
        자신.전문제어 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 자신.전문제어.bind(('127.0.0.1', 0))
        자신.conexión_control.settimeout(30); 자신.전문제어.settimeout(30)
        자신.TCP_porto = 자신.conexión_control.getsockname()[1]; 자신.UDP_porto = 자신.전문제어.getsockname()[1]
        자신.오류들 = []; 자신.수신됨 = {}
        def conexión_control():
            try:
                conexión_e05f319b, _ = 자신.conexión_control.accept()
                with conexión_e05f319b:
                    conexión_e05f319b.settimeout(5); datos = bytearray()
                    while b'\n' not in datos:
                        조각 = conexión_e05f319b.recv(512)
                        if not 조각: raise RuntimeError('TCP EOF before request')
                        datos.extend(조각)
                    자신.수신됨['tcp'] = bytes(datos); conexión_e05f319b.sendall(datos)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        def 전문제어():
            try:
                datos, punto_VALOR = 자신.전문제어.recvfrom(512); 자신.수신됨['udp'] = datos; 자신.전문제어.sendto(datos, punto_VALOR)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        자신.작업가닥들 = [threading.Thread(target=Ficheiro_introdución, daemon=True) for Ficheiro_introdución in (conexión_control, 전문제어)]
        for Terminal_introdución in 자신.작업가닥들: Terminal_introdución.start()
        return 자신

    def __exit__(자신, *argumento_MATRIZ):
        자신.conexión_control.close(); 자신.전문제어.close()
        for Terminal_introdución in 자신.작업가닥들: Terminal_introdución.join(timeout=1)
