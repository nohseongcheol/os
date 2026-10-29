#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'tomhas_dàta', 'builtins': '내장연산', 'header': 'bann_cinn_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'gnìomhaich_àithne', 'flags': '설정비트', 'path': 'Slighe', 'p': 'dàta_suidhich', 'cc': '시언어번역기', 'obj': 'faidhle_uidhe', 'flag': 'roghainnean_VALUE', 'ld': '연결편집기', 'objects': 'ceann_uidhe_faidhlichean', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'freumh_ADDRESS', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Ainm', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
