#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/carga_Ficheiros.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('carga_Ficheiros', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('carga_Ficheiros')
    대응 = {'data': 'datos', 'i': '순번', 'name': 'Nome', 'c': 'código_de_carácter', 'p': 'datos_cargo', 'args': 'argumento_MATRIZ'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
