#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'tomhas_sonraí', 'builtins': '내장연산', 'header': 'Ceanntásc_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'Rith_ordú', 'flags': '설정비트', 'path': 'CONAIR', 'p': 'sonraí_suíomh', 'cc': '시언어번역기', 'obj': 'comhad_sprice', 'flag': 'Socruithe_VALUE', 'ld': '연결편집기', 'objects': 'sprioc_Comhaid', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'fréamh_ADDRESS', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Ainm', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
