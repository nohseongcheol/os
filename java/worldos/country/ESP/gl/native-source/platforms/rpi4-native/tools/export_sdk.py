#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/개발꾸러미내보내기.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('개발꾸러미내보내기')
    대응 = {'out': 'medida_datos', 'obj': 'ficheiro_de_destino', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Arquivo', 'main': 'Executar_2', 'posix': '포직스경로', 'files': 'Ficheiro_Lista', 'source': '원본자료', 'name': 'Nome', 'target': 'obxectivo_VALOR', 'ROOT': 'Project_raíz', 'destination': 'destino_datos_ENDEREZO', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
