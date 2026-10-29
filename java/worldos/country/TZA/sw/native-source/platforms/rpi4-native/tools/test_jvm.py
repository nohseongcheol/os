#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/자바가상기계시험.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'tungo_data', 'actual': '실제결과', 'match': '일치', 'payload': 'data_muhimu_data', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'endesha', 'ROOT': '기준', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'tabaka_njia', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'Jina', 'jar': '자바꾸러미', 'report': 'uhakikishi_ripoti', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
