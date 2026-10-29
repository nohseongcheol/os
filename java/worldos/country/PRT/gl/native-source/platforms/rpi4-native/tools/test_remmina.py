#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/원격한글시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Executar_2', 'profile': 'Perfil', 'focused': 'Importantes', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'servidor_VALOR', 'log': 'LOG_fila', 'args': 'argumento_MATRIZ', 'deadline': '마감시각', 'data': 'datos', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Executar_2', 'ready': '준비완료', 'found': 'ACHAR_medida', 'guest': 'convidado', 'ROOT': 'Project_raíz', 'marker': '확인표시', 'text': 'Texto', 'out': 'medida_datos', 'env': '환경', 'f': 'Ficheiro_introdución', 'port': 'número_do_porto', 'offset': 'DESPRAZAMENTO_VALOR', 'version': '판번호', 'p': 'datos_cargo', 'selector': '준비선택기', 'xvfb': 'virtual_mostrar', 'display': 'pantalla', 'n': 'elemento_CONTAR', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Nome', 'window': 'Xanela', 'report': 'validación_informe', 'work': '작업경로'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
