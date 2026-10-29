#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'x_chomhordanáid', 's': 'teaghrán_sonraí', 'i': '순번', 'sel': 'roghnóir_a916db4e', 'seconds': '초단위', 'log': 'LOG_ró', 'data': 'sonraí', 'at': '현재위치', 'send': 'seol', 'main': 'Rith_2', 'req': 'iarratas_HTTP_VALUE', 'hot': 'aicearra_VALUE', 'pump': 'hanla_ócáid', 'ROOT': 'teilgean_fréamh', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'Ordú', 'shell': 'blaosc', 'f': 'comhad_iontráil', 'click': 'cliceáil_cnaipe', 'k': '셋째순번', 'c': 'pointe_cóid', 'r': '반환값', 'p': 'sonraí_suíomh', 'command_mode': 'ordú_mód', 'end': 'cuir_deireadh_le_OFFSET', 'classes': 'aicme_cosán', 'key': '누름값', 'y': '세로좌표', 'result': 'tomhas', 'report': 'bailíochtú_tuairisc', 'dest': 'sprioc_VALUE_suíomh', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
