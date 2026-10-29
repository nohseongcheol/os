#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/흐름시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('흐름시험')
    대응 = {'out': 'medida_datos', 'main': 'Executar_2', 'ROOT': 'Project_raíz', 'p': 'datos_cargo', 'text': 'Texto', 'report': 'validación_informe'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
