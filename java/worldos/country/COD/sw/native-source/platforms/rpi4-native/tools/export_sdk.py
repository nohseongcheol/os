#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/hamisha_SDK.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('hamisha_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('hamisha_SDK')
    대응 = {'out': '결과자료', 'obj': 'faili_fikio', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Hifadhi_eb6be19d', 'main': 'endesha', 'posix': '포직스경로', 'files': 'faili_Orodha', 'source': '원본자료', 'name': 'Jina', 'target': 'lengo', 'ROOT': '기준', 'destination': 'fikio_data_anwani', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
