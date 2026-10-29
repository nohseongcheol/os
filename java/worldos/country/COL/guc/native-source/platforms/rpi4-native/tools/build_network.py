#!/usr/bin/env python3
"""기존 wopu_a_ttaaleemüin 호환 ekeroliaa_o_uchikanain. 실제 구현: ../도구/akompiraajaa_kusu.py"""
import importlib as 가져오기
import sys as a_yatawajiraaya_a_laülaasü_ajutuu
from pathlib import Path as wopu_a_ttaaleemüin
a_yatawajiraaya_a_laülaasü_ajutuu.path.insert(0, str(wopu_a_ttaaleemüin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('akompiraajaa_kusu', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('akompiraajaa_kusu')
    대응 = {'obj': 'anaajaalaa_ama_anamüinjatü', 'objects': '목적파일들', 'library': 'anaajaalee', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': '파일목록', 'source': '원본자료', 'run': '실행', 'flags': '설정비트', 'path': 'wopu_a_ttaaleemüin', 'build_network': '통신망만들기', 'cc': '시언어번역기', 'ar': 'anaajawaa_a_yataaya'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
