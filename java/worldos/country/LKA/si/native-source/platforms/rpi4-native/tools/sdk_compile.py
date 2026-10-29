#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/개발꾸러미번역.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'ගමනාන්ත_ගොනුව', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'ක්_රියාත්මක_කරන්න_2', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': '인수해석기', 'language': 'භාෂාව', 'work': '작업경로', 'args': 'විස්තාරකය_ආරා_ව'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
