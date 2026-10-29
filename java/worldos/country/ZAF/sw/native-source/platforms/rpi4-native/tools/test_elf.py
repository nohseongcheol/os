#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/실행파일시험.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'programu_kichwa_Chipua', 'offset': 'Chipua_thamani', 'invalid': 'batili_data', 'path': 'njia', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'umbiza_b87fd068', 'main': 'endesha', 'content': 'maudhui_thamani', 'source': '원본자료', 'name': 'Jina', 'reference': 'Kulinganisha_mpango', 'ROOT': '기준', 'value': 'thamani', 'report': 'uhakikishi_ripoti'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
