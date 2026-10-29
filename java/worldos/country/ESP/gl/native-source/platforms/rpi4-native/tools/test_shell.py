#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/셸시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'X_coordenada', 'msg': 'Rede_correo', 'i': '순번', 'reply': 'resposta', 'call': '호출', 'args': 'argumento_MATRIZ', 'chunk': '조각', 'data': 'datos', 'proc': 'Proceso', 'long_text': '긴글', 'restored': '복원자료', 'send': 'enviar', 'file': 'Ficheiro', 'main': 'Executar_2', 'found': 'ACHAR_medida', 'ROOT': 'Project_raíz', 'text': 'Texto', 'marker': '확인표시', 'command': 'Orde', 'expected': '예상결과', 'pixel': 'píxel', 'shell': 'shell', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'finalizar_DESPRAZAMENTO', 'image': 'IMAXE', 'key': '누름값', 'y': 'Y_coordenada', 'output': '출력결과', 'result': 'RESULTANTE', 'client': 'cliente', 'line': 'Liña', 'stream': 'fluxo_VALOR', 'name': 'Nome', 'value': 'VALOR', 'receive': '수신하기', 'report': 'validación_informe', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
