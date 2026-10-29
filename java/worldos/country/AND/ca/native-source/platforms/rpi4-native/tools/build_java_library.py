#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/자바라이브러리빌드.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('자바라이브러리빌드')
    대응 = {'header': 'Capçalera_VALOR', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'càrrega_dades', 'src': '원본주소', 'run': 'Executa_ordre', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'Classe_camí', 'dist': '배포경로', 'archive': 'Arxiu', 'output': '출력결과', 'root': 'rel_ADREÇA', 'name': 'Nom', 'jar': '자바꾸러미', 'b': 'SEGON_VALOR', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
