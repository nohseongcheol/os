#!/usr/bin/env python3
"""기존 wopu_a_ttaaleemüin 호환 ekeroliaa_o_uchikanain. 실제 구현: ../도구/파일실행.py"""
import importlib as 가져오기
import sys as a_yatawajiraaya_a_laülaasü_ajutuu
from pathlib import Path as wopu_a_ttaaleemüin
a_yatawajiraaya_a_laülaasü_ajutuu.path.insert(0, str(wopu_a_ttaaleemüin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('파일실행', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일실행')
    대응 = {'timeout': '시간제한', 's': 'kaleena_atijaaya', 'i': '순번', 'match': '일치', 'files': '파일목록', 'program': 'akumajiaa', 'executable': '실행가능파일', 'args': 'ajutuu_matüriisü', 'chunk': '조각', 'data': 'atijaaya', 'proc': '실행과정', 'send': 'ajütaa', 'main': '시작', 'marker': '확인표시', 'command': 'aluwataaya', 'include': '포함항목', 'dumped': '갈무리자료', 'run': '실행', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Aneekuui', 'kind': 'akotchiraayanüliee_ajutuu', 'selector': '준비선택기', 'upload_data': 'o_ote_eraa_atijaaya', 'end': '끝위치', 'n': '개수', 'd': 'jalamüinjatü_atijaaya', 'key': '누름값', 'output': '출력결과', 'line': 'liinia', 'name': '이름', 'upload_name': '올릴이름', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
