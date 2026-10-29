#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/generar_PYTHON.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('generar_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('generar_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'Arxiu', 'SHA256': 'validació_hash', 'build_python': 'Crear_PYTHON', 'root': 'rel_ADREÇA', 'source': '원본자료', 'name': 'Nom', 'path': 'Camí', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'membre'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
