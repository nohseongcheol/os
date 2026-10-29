#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Umutwengaruka_agaciro', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'ibitwarwa_amakurushingiro', 'src': '원본주소', 'run': 'gukora_ibwiriza', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'icyiciro_inzira', 'dist': '배포경로', 'archive': 'gushyingura', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Izina', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
