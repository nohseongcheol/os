#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'tomhas_sonraí', 'expected': '예상결과', 'phoff': 'clár_Ceanntásc_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'neamhbhailí_sonraí', 'path': 'CONAIR', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'tomhas', 'format_': 'formáid_b87fd068', 'main': 'Rith_2', 'content': 'Inneachar_VALUE', 'source': '원본자료', 'name': 'Ainm', 'reference': '비교기준', 'ROOT': 'teilgean_fréamh', 'value': 'VALUE', 'report': 'bailíochtú_tuairisc'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
