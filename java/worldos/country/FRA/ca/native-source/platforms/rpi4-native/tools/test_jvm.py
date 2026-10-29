#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/자바가상기계시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'cadena_dades', 'actual': 'real_mesura', 'match': '일치', 'payload': 'càrrega_dades', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Executa_2', 'ROOT': 'Project_rel', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': 'incloure', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Completades_quantitat', 'classes': 'Classe_camí', 'output': '출력결과', 'result': 'RESULTAT', 'cmd': '명령인수', 'name': 'Nom', 'jar': '자바꾸러미', 'report': 'validació_informe', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
