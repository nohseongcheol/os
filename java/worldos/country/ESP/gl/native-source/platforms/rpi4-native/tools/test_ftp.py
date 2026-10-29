#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/파일전송시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'carga_datos_60367a51', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'datos', 'proc': 'Proceso', 'code': 'instrución_SECUENCIA', 'linux': '리눅스파일', 'archive': 'Arquivo', 'main': 'Executar_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'estático_fonte', 'java_source': '자바원문', 'echo': 'eco_servidor_introdución', 'ROOT': 'Project_raíz', 'text': 'Texto', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Orde', 'out': 'medida_datos', 'expected': '예상결과', 'server_source': 'servidor_fonte', 'shell': 'shell', 'upload': 'carga_Ficheiros', 'transcript': '대화기록', 'port': 'número_do_porto', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ponte', 'selector': '준비선택기', 'end': 'finalizar_DESPRAZAMENTO', 'e': '보조항목', 'ftp': 'transferencia_de_ficheiros_conexión', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'punto_VALOR', 'result': 'RESULTANTE', 'unchanged': '보존자료', 'line': 'Liña', 'server_tcp_port': 'servidor_fluxo_porto', 'source': '원본자료', 'NetworkBridge': 'Rede_ponte', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'validación_informe'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
