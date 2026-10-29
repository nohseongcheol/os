#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/Rede_ponte.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('Rede_ponte', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('Rede_ponte')
    대응 = {'response': 'resposta_1262b476', 'parts': 'camiño_compoñente', 's': 'cadea_datos', 'i': '순번', 'close': 'Pechar', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'introdución_VALOR', 'flags': 'configuración_Servizo_de_transferencia_intelixente_en_segundo_plano', 'ftp_port': 'transferencia_de_ficheiros_número_do_porto', 'args': 'argumento_MATRIZ', 'server': 'servidor_VALOR', 'data': 'datos', 'ethernet_input': '이더넷입력', 'trace_packet': 'traza_paquete', 'GATEWAY': '관문기계주소', 'rule': 'regra_VALOR', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'hospedar', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'convidado', 'destination': 'destino_datos_ENDEREZO', 'ethernet_port': 'porto_Ethernet', 'b': 'SEGUNDO_VALOR', 'MAC': 'máquina_ENDEREZO', 'arp': 'ENDEREZO_resolución_paquete', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Ciclo_VALOR', 'port': 'número_do_porto', 'offset': 'DESPRAZAMENTO_VALOR', 'readable': '읽을수있음', 'c': 'código_de_carácter', 'p': 'datos_cargo', 'writers': '쓰기대상들', 'IP': 'enderezo_de_internet_VALOR', 'e': '보조항목', 'n': 'elemento_CONTAR', 'packet': 'paquete_datos', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Rede_ponte', 'window': 'Xanela', 'capture': 'capturar'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
