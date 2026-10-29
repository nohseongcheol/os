#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/셸시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'X_coordenada', 'msg': 'xarxa_correu', 'i': '순번', 'reply': 'resposta', 'call': '호출', 'args': 'arg_MATRIU', 'chunk': '조각', 'data': 'dades', 'proc': 'Procés', 'long_text': '긴글', 'restored': '복원자료', 'send': 'enviar', 'file': 'Fitxer', 'main': 'Executa_2', 'found': 'Cerca_mesura', 'ROOT': 'Project_rel', 'text': 'SMS', 'marker': '확인표시', 'command': 'Ordre', 'expected': '예상결과', 'pixel': 'píxel', 'shell': 'shell', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'finalitzar_DESPLAÇAMENT', 'image': 'IMATGE', 'key': '누름값', 'y': 'Y_coordenada', 'output': '출력결과', 'result': 'RESULTAT', 'client': 'client', 'line': 'línia', 'stream': 'flux_VALOR', 'name': 'Nom', 'value': 'VALOR', 'receive': 'rebre_correu', 'report': 'validació_informe', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
