#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/바탕화면시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('바탕화면시험')
    대응 = {'x': 'X_coordenada', 'typing': '글자입력', 'message': '알림문', 'start': 'Executa_2', 'down': '누르는중', 'exact': 'IGUAL_VALOR', 'i': '순번', 'press': 'prémer_Clau', 'rectangles': '사각형들', 'sym': 'símbol', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Procés', 'data': 'dades', 'main': 'Executa_2', 'w': '너비값', 'init': '초기값', 'block': 'dades_bloquejar', 'ROOT': 'Project_rel', 'text': 'SMS', 'marker': '확인표시', 'report': 'validació_informe', 'until': '까지', 'clipboard': 'Porta_retalls_VALOR', 'dst': 'destinació_ADREÇA', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'número_de_port', 'offset': 'DESPLAÇAMENT_VALOR', 'h': '높이값', 'src': '원본주소', 'event': 'Esdeveniment', 'encoding': 'joc_de_caràcters', 'size': 'Mida', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_coordenada', 'output': '출력결과', 'symbol': 'símbol_VALOR', 'client': 'client', 'char': 'caràcter_dades', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
