#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/실행파일시험.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'jëfekaay_Tur_Randal', 'offset': 'Randal_xëyma', 'invalid': 'baaxul_mbir', 'path': 'Yoonu_jëmale', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'dayo_b87fd068', 'main': 'daw', 'content': 'Këmb_xëyma', 'source': '원본자료', 'name': 'tur_253d1510', 'reference': '비교기준', 'ROOT': '기준', 'value': 'xëyma', 'report': 'wéral_tënk'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
