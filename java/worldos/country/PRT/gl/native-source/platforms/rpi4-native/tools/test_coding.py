#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/코딩시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('코딩시험')
    대응 = {'out': 'medida_datos', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Executar_2', 'elf': '실행파일', 'run': 'executar_comando', 'name': 'Nome', 'path': 'CAMIÑO', 'p': 'datos_cargo', 'ROOT': 'Project_raíz', 'report': 'validación_informe', 'args': 'argumento_MATRIZ'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
