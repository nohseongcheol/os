#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/실행파일시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('실행파일시험')
    대응 = {'out': 'mesura_dades', 'expected': '예상결과', 'phoff': 'programa_Capçalera_DESPLAÇAMENT', 'offset': 'DESPLAÇAMENT_VALOR', 'invalid': 'invàlid_dades', 'path': 'Camí', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'RESULTAT', 'format_': 'format_b87fd068', 'main': 'Executa_2', 'content': 'contingut_VALOR', 'source': '원본자료', 'name': 'Nom', 'reference': 'Comparació_referència', 'ROOT': 'Project_rel', 'value': 'VALOR', 'report': 'validació_informe'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
