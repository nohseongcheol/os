#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/executar_comando.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('executar_comando', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('executar_comando')
    대응 = {'supported': '지원목록', 'parser': 'analizador', 'qemu': '모의기계', 'run_desktop': 'executar_escritorio', 'main': 'Executar_2', 'host': 'hospedar', 'status': 'Estado_VALOR', 'NetworkBridge': 'Rede_ponte', 'ROOT': 'Project_raíz', 'bridge': 'ponte', 'loader': '적재기', 'base': 'Fondo_VALOR', 'options': 'Opcións', 'binary': 'binario', 'args': 'argumento_MATRIZ', 'command': 'Orde'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
