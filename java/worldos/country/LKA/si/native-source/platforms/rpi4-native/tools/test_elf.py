#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/실행파일시험.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'යෙදු_ශීර්ෂය_ඕෆ්සෙට්', 'offset': 'ඕෆ්සෙට්_අගය', 'invalid': 'අවලංගු_දත්ත', 'path': 'මාර්_ගය', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'හැඩතලය_b87fd068', 'main': 'ක්_රියාත්මක_කරන්න_2', 'content': 'අන්තර්ගතය_අගය', 'source': '원본자료', 'name': 'නම', 'reference': '비교기준', 'ROOT': '기준', 'value': 'අගය', 'report': 'වලංගුකරණය_වාර්තාව'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
