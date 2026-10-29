#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/시언어번역기빌드.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('시언어번역기빌드')
    대응 = {'out': 'mesura_dades', 'builtins': '내장연산', 'header': 'Capçalera_VALOR', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'Executa_ordre', 'flags': 'configuració_Servei_de_transferència_intel_ligent_en_segon_terme', 'path': 'Camí', 'p': 'dades_càrrec', 'cc': '시언어번역기', 'obj': 'fitxer_de_destinació', 'flag': 'Configuració_VALOR', 'ld': '연결편집기', 'objects': 'destinació_Fitxers', 'repo': 'dipòsit_camí', 'v': '임시값', 'upstream': 'superior', 'root': 'rel_ADREÇA', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nom', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
