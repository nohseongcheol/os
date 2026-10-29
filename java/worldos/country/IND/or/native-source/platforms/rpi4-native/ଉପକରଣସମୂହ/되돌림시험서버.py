"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class 되돌림시험서버:
    def __enter__(자신):
        자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ = socket.socket(); 자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ.bind(('127.0.0.1', 0)); 자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ.listen(1)
        자신.전문제어 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 자신.전문제어.bind(('127.0.0.1', 0))
        자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ.settimeout(30); 자신.전문제어.settimeout(30)
        자신.ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ = 자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ.getsockname()[1]; 자신.전문접속번호 = 자신.전문제어.getsockname()[1]
        자신.오류들 = []; 자신.수신됨 = {}
        def ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ():
            try:
                ସଂଯୋଗ_e05f319b, _ = 자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ.accept()
                with ସଂଯୋଗ_e05f319b:
                    ସଂଯୋଗ_e05f319b.settimeout(5); ଡାଟା = bytearray()
                    while b'\n' not in ଡାଟା:
                        조각 = ସଂଯୋଗ_e05f319b.recv(512)
                        if not 조각: raise RuntimeError('TCP EOF before request')
                        ଡାଟା.extend(조각)
                    자신.수신됨['tcp'] = bytes(ଡାଟା); ସଂଯୋଗ_e05f319b.sendall(ଡାଟା)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        def 전문제어():
            try:
                ଡାଟା, ସମକକ୍ଷ_ମୂଲ୍ୟ = 자신.전문제어.recvfrom(512); 자신.수신됨['udp'] = ଡାଟା; 자신.전문제어.sendto(ଡାଟା, ସମକକ୍ଷ_ମୂଲ୍ୟ)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        자신.작업가닥들 = [threading.Thread(target=ଫାଇଲ୍_ଏଣ୍ଟ୍ରି, daemon=True) for ଫାଇଲ୍_ଏଣ୍ଟ୍ରି in (ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ, 전문제어)]
        for ଟର୍ମିନାଲ୍_ଏଣ୍ଟ୍ରି in 자신.작업가닥들: ଟର୍ମିନାଲ୍_ଏଣ୍ଟ୍ରି.start()
        return 자신

    def __exit__(자신, *ଯୁକ୍ତି_ଆରେ):
        자신.ସଂଯୋଗ_ନିୟନ୍ତ୍ରଣ.close(); 자신.전문제어.close()
        for ଟର୍ମିନାଲ୍_ଏଣ୍ଟ୍ରି in 자신.작업가닥들: ଟର୍ମିନାଲ୍_ଏଣ୍ଟ୍ରି.join(timeout=1)
