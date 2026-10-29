#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/예제빌드.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'dosiye_Urutonde', 'java': '자바실행', 'run': 'gukora_ibwiriza', 'path': 'Inzira', 'p': '자료위치', 'readme': 'NSOMA', 'build_java_library': '자바라이브러리만들기', 'code': 'ibwiriza_URUKURIKIRANE', 'index': '색인', 'classes': 'icyiciro_inzira', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Ibirimo_agaciro', 'source': '원본자료', 'name': 'Izina', 'target': 'gusimbuza_igishya', 'manifest': '꾸러미명세', 'language': 'Ururimi'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
