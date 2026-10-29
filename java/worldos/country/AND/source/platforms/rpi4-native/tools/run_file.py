#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/Executa_arxiu.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('Executa_arxiu', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('Executa_arxiu')
    대응 = {'timeout': '시간제한', 's': 'cadena_dades', 'i': '순번', 'match': '일치', 'files': 'arxiu_Llista', 'program': 'programa', 'executable': '실행가능파일', 'args': 'arg_MATRIU', 'chunk': '조각', 'data': 'dades', 'proc': 'Procés', 'send': 'enviar', 'main': 'Executa_2', 'marker': '확인표시', 'command': 'Ordre', 'include': 'incloure', 'dumped': '갈무리자료', 'run': 'Executa_ordre', 'p': 'dades_càrrec', 'parser': 'analitzador', 'options': 'Opcions', 'kind': 'Categoria_VALOR', 'selector': '준비선택기', 'upload_data': 'pujar_dades', 'end': 'finalitzar_DESPLAÇAMENT', 'n': 'element_COMPT', 'd': 'destinació_dades', 'key': '누름값', 'output': '출력결과', 'line': 'línia', 'name': 'Nom', 'upload_name': 'pujar_nom', 'receive': 'rebre_correu'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
