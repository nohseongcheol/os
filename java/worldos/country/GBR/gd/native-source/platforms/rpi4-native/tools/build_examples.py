#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'tomhas_dàta', 'build_examples': '예제만들기', 'files': 'faidhle_Liosta', 'java': '자바실행', 'run': 'gnìomhaich_àithne', 'path': 'Slighe', 'p': 'dàta_suidhich', 'readme': 'LEUGHMI', 'build_java_library': '자바라이브러리만들기', 'code': 'treòrachadh_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'clas_slighe', 'repo': '저장소경로', 'root': 'freumh_ADDRESS', 'content': 'susbaint_VALUE', 'source': '원본자료', 'name': 'Ainm', 'target': 'targaid', 'manifest': '꾸러미명세', 'language': 'cànan'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
