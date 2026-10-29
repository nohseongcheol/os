"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class eco_acessório:
    def __enter__(자신):
        자신.conexão_visual = socket.socket(); 자신.conexão_visual.bind(('127.0.0.1', 0)); 자신.conexão_visual.listen(1)
        자신.datagrama_visual = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 자신.datagrama_visual.bind(('127.0.0.1', 0))
        자신.conexão_visual.settimeout(30); 자신.datagrama_visual.settimeout(30)
        자신.porta_TCP = 자신.conexão_visual.getsockname()[1]; 자신.UDP_porta = 자신.datagrama_visual.getsockname()[1]
        자신.오류들 = []; 자신.수신됨 = {}
        def conexão_visual():
            try:
                conexão_e05f319b, _ = 자신.conexão_visual.accept()
                with conexão_e05f319b:
                    conexão_e05f319b.settimeout(5); dados = bytearray()
                    while b'\n' not in dados:
                        fragmento_VALOR = conexão_e05f319b.recv(512)
                        if not fragmento_VALOR: raise RuntimeError('TCP EOF before request')
                        dados.extend(fragmento_VALOR)
                    자신.수신됨['tcp'] = bytes(dados); conexão_e05f319b.sendall(dados)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        def datagrama_visual():
            try:
                dados, par_VALOR = 자신.datagrama_visual.recvfrom(512); 자신.수신됨['udp'] = dados; 자신.datagrama_visual.sendto(dados, par_VALOR)
            except Exception as 보조항목: 자신.오류들.append(str(보조항목))
        자신.작업가닥들 = [threading.Thread(target=Arquivo_entrada, daemon=True) for Arquivo_entrada in (conexão_visual, datagrama_visual)]
        for Terminal_entrada in 자신.작업가닥들: Terminal_entrada.start()
        return 자신

    def __exit__(자신, *argumento_MATRIZ):
        자신.conexão_visual.close(); 자신.datagrama_visual.close()
        for Terminal_entrada in 자신.작업가닥들: Terminal_entrada.join(timeout=1)
