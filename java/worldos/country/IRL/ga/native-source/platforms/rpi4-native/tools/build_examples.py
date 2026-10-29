#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'tomhas_sonraí', 'build_examples': '예제만들기', 'files': 'comhad_Liosta', 'java': '자바실행', 'run': 'Rith_ordú', 'path': 'CONAIR', 'p': 'sonraí_suíomh', 'readme': 'LÉIGHMÉ', 'build_java_library': '자바라이브러리만들기', 'code': 'treoir_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'aicme_cosán', 'repo': '저장소경로', 'root': 'fréamh_ADDRESS', 'content': 'Inneachar_VALUE', 'source': '원본자료', 'name': 'Ainm', 'target': 'sprioc', 'manifest': '꾸러미명세', 'language': 'Teanga'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
