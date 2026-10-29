"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class 되돌림시험서버:
    def __enter__(자신):
        자신.връзка_контрол = socket.socket(); 자신.връзка_контрол.bind(('127.0.0.1', 0)); 자신.връзка_контрол.listen(1)
        자신.дейтаграма_контрол = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 자신.дейтаграма_контрол.bind(('127.0.0.1', 0))
        자신.връзка_контрол.settimeout(30); 자신.дейтаграма_контрол.settimeout(30)
        자신.연결접속번호 = 자신.връзка_контрол.getsockname()[1]; 자신.전문접속번호 = 자신.дейтаграма_контрол.getsockname()[1]
        자신.오류들 = []; 자신.수신됨 = {}
        def връзка_контрол():
            try:
                връзка_e05f319b, _ = 자신.връзка_контрол.accept()
                with връзка_e05f319b:
                    връзка_e05f319b.settimeout(5); данни = bytearray()
                    while b'\n' not in данни:
                        조각 = връзка_e05f319b.recv(512)
                        if not 조각: raise RuntimeError('TCP EOF before request')
                        данни.extend(조각)
                    자신.수신됨['tcp'] = bytes(данни); връзка_e05f319b.sendall(данни)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        def дейтаграма_контрол():
            try:
                данни, крайно_устройство_стойност = 자신.дейтаграма_контрол.recvfrom(512); 자신.수신됨['udp'] = данни; 자신.дейтаграма_контрол.sendto(данни, крайно_устройство_стойност)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        자신.작업가닥들 = [threading.Thread(target=Файл_запис, daemon=True) for Файл_запис in (връзка_контрол, дейтаграма_контрол)]
        for Терминал_запис in 자신.작업가닥들: Терминал_запис.start()
        return 자신

    def __exit__(자신, *аргумент_масив):
        자신.връзка_контрол.close(); 자신.дейтаграма_контрол.close()
        for Терминал_запис in 자신.작업가닥들: Терминал_запис.join(timeout=1)
