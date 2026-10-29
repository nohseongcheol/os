#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/셸시험.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_chomhordanáid', 'msg': 'Líonra_teachtaireacht', 'i': '순번', 'reply': 'freagair', 'call': '호출', 'args': 'argóint_ARRAY', 'chunk': '조각', 'data': 'sonraí', 'proc': 'Próiseas', 'long_text': '긴글', 'restored': '복원자료', 'send': 'seol', 'file': 'Comhad', 'main': 'Rith_2', 'found': 'SEARCH_tomhas', 'ROOT': 'teilgean_fréamh', 'text': 'Téacs', 'marker': '확인표시', 'command': 'Ordú', 'expected': '예상결과', 'pixel': 'picteilín', 'shell': 'blaosc', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'cuir_deireadh_le_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'tomhas', 'client': 'cliant', 'line': 'Líne', 'stream': 'sruth_VALUE', 'name': 'Ainm', 'value': 'VALUE', 'receive': '수신하기', 'report': 'bailíochtú_tuairisc', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
