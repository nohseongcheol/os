#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'kichwa_thamani', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'data_muhimu_data', 'src': '원본주소', 'run': 'tekeleza_amri', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'tabaka_njia', 'dist': '배포경로', 'archive': 'Hifadhi_eb6be19d', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Jina', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
