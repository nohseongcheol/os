#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/되돌림시험서버.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('되돌림시험서버')
    대응 = {'data': 'datos', 'e': '보조항목', 'connection': 'conexión_e05f319b', 'f': 'Ficheiro_introdución', 'peer': 'punto_VALOR', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_introdución', 'tcp': 'conexión_control', 'EchoFixture': '되돌림시험서버', 'args': 'argumento_MATRIZ', 'chunk': '조각'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
