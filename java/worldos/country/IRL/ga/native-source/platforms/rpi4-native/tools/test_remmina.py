#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Rith_2', 'profile': 'Próifíl', 'focused': 'Fócasaithe', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'freastalaí_VALUE', 'log': 'LOG_ró', 'args': 'argóint_ARRAY', 'deadline': '마감시각', 'data': 'sonraí', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Rith_2', 'ready': '준비완료', 'found': 'SEARCH_tomhas', 'guest': 'aoi', 'ROOT': 'teilgean_fréamh', 'marker': '확인표시', 'text': 'Téacs', 'out': 'tomhas_sonraí', 'env': '환경', 'f': 'comhad_iontráil', 'port': 'uimhir_phoirt', 'offset': 'OFFSET_VALUE', 'version': 'uimhir_an_leagain', 'p': 'sonraí_suíomh', 'selector': 'roghnóir', 'xvfb': 'fíorúil_taispeáin', 'display': 'taispeáint', 'n': 'mír_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Ainm', 'window': 'fuinneog', 'report': 'bailíochtú_tuairisc', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
