#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/예제빌드.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('예제빌드')
    대응 = {'out': 'mesura_dades', 'build_examples': '예제만들기', 'files': 'arxiu_Llista', 'java': '자바실행', 'run': 'Executa_ordre', 'path': 'Camí', 'p': 'dades_càrrec', 'readme': 'LLEGIU_ME', 'build_java_library': '자바라이브러리만들기', 'code': 'instrucció_SEQÜÈNCIA', 'index': 'Cerca_INDEX', 'classes': 'Classe_camí', 'repo': 'dipòsit_camí', 'root': 'rel_ADREÇA', 'content': 'contingut_VALOR', 'source': '원본자료', 'name': 'Nom', 'target': 'objectiu', 'manifest': '꾸러미명세', 'language': 'Idioma'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
