#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/compilar_PYTHON.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('compilar_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('compilar_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'Arquivo', 'SHA256': 'validación_hash', 'build_python': 'crear_PYTHON', 'root': 'raíz_ENDEREZO', 'source': '원본자료', 'name': 'Nome', 'path': 'CAMIÑO', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'membro'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
