#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/tabax_mbaal.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('tabax_mbaal', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('tabax_mbaal')
    대응 = {'obj': 'jëmu', 'objects': 'jëmmukaay_Fisiye_yi', 'library': 'daaray_téere', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'bara_denc_lim', 'source': '원본자료', 'run': 'def_ndigel', 'flags': '설정비트', 'path': 'Yoonu_jëmale', 'build_network': 'sos_mbaal_48d29d6d', 'cc': '시언어번역기', 'ar': 'denc_jumtukaay'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
