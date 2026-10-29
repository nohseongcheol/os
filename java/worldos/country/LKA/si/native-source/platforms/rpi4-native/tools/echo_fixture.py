#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/되돌림시험서버.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'දත්ත', 'e': '보조항목', 'connection': 'සබැඳුම_e05f319b', 'f': 'ගොනුව_පිවිසුම', 'peer': 'සමානයා_අගය', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'සබැඳුම_පාලකය', 'EchoFixture': '되돌림시험서버', 'args': 'විස්තාරකය_ආරා_ව', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
