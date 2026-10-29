"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class 되돌림시험서버:
    def __enter__(자신):
        자신.연결제어 = socket.socket(); 자신.연결제어.bind(('127.0.0.1', 0)); 자신.연결제어.listen(1)
        자신.전문제어 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 자신.전문제어.bind(('127.0.0.1', 0))
        자신.연결제어.settimeout(30); 자신.전문제어.settimeout(30)
        자신.연결접속번호 = 자신.연결제어.getsockname()[1]; 자신.전문접속번호 = 자신.전문제어.getsockname()[1]
        자신.오류들 = []; 자신.수신됨 = {}
        def 연결제어():
            try:
                접속, _ = 자신.연결제어.accept()
                with 접속:
                    접속.settimeout(5); 자료 = bytearray()
                    while b'\n' not in 자료:
                        조각 = 접속.recv(512)
                        if not 조각: raise RuntimeError('TCP EOF before request')
                        자료.extend(조각)
                    자신.수신됨['tcp'] = bytes(자료); 접속.sendall(자료)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        def 전문제어():
            try:
                자료, 상대 = 자신.전문제어.recvfrom(512); 자신.수신됨['udp'] = 자료; 자신.전문제어.sendto(자료, 상대)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        자신.작업가닥들 = [threading.Thread(target=파일항목, daemon=True) for 파일항목 in (연결제어, 전문제어)]
        for 터미널항목 in 자신.작업가닥들: 터미널항목.start()
        return 자신

    def __exit__(자신, *인수배열):
        자신.연결제어.close(); 자신.전문제어.close()
        for 터미널항목 in 자신.작업가닥들: 터미널항목.join(timeout=1)
