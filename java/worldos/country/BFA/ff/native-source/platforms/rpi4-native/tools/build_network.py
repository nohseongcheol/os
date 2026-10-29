#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/tafde_laylaytol.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('tafde_laylaytol', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('tafde_laylaytol')
    대응 = {'obj': 'tiindaare_fiilde', 'objects': '목적파일들', 'library': 'defterdu', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'fiilde_Doggol', 'source': '원본자료', 'run': '실행', 'flags': '설정비트', 'path': 'laawol', 'build_network': '통신망만들기', 'cc': '시언어번역기', 'ar': 'ƴeewtirde_kuutorgal'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
