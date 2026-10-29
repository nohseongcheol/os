#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/개발꾸러미내보내기.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('개발꾸러미내보내기')
    대응 = {'out': 'mesura_dades', 'obj': 'fitxer_de_destinació', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Arxiu', 'main': 'Executa_2', 'posix': '포직스경로', 'files': 'arxiu_Llista', 'source': '원본자료', 'name': 'Nom', 'target': 'objectiu', 'ROOT': 'Project_rel', 'destination': 'destinació_dades_ADREÇA', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
