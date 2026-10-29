#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/예제빌드.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'faili_Orodha', 'java': '자바실행', 'run': 'tekeleza_amri', 'path': 'njia', 'p': '자료위치', 'readme': 'NISOME', 'build_java_library': '자바라이브러리만들기', 'code': 'agizo_MFUATANO', 'index': '색인', 'classes': 'tabaka_njia', 'repo': 'uwekaji_njia', 'root': '뿌리주소', 'content': 'maudhui_thamani', 'source': '원본자료', 'name': 'Jina', 'target': 'lengo', 'manifest': '꾸러미명세', 'language': 'Lugha'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
