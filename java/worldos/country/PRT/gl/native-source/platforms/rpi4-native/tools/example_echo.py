#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/예제되돌림서버.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('예제되돌림서버')
    대응 = {'data': 'datos', 'sock': '소켓', 'tcp_port': 'TCP_porto', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': 'eco_servidor_introdución', 'TCP': 'agarradoira_conexión_solicitude', 'EchoServers': 'eco_Servidores', 'parser': 'analizador', 'server': 'servidor_VALOR', 'udp_port': 'UDP_porto', 'args': 'argumento_MATRIZ'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
