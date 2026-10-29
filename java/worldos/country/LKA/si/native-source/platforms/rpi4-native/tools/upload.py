#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/උඩුගත_කරන්න_ගොනු.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('උඩුගත_කරන්න_ගොනු', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('උඩුගත_කරන්න_ගොනු')
    대응 = {'data': 'දත්ත', 'i': '순번', 'name': 'නම', 'c': 'අනුලකුණු_කේතය', 'p': '자료위치', 'args': 'විස්තාරකය_ආරා_ව'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
