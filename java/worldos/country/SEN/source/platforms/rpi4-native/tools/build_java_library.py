#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Tur_xëyma', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'njoxe_yu_solowu_mbir', 'src': '원본주소', 'run': 'def_ndigel', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'maas_Yoonu_jëmale', 'dist': '배포경로', 'archive': 'denc', 'output': '출력결과', 'root': '뿌리주소', 'name': 'tur_253d1510', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
