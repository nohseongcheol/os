#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('ක්_රියාත්මක_කරන්න_විධානය', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ක්_රියාත්මක_කරන්න_විධානය')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ධාවනය_කරන්න_වැඩතලය', 'main': 'ක්_රියාත්මක_කරන්න_2', 'host': 'ධාරකය', 'status': 'තත්වය_අගය', 'NetworkBridge': 'ජාලය_පාලම', 'ROOT': '기준', 'bridge': 'පාලම', 'loader': '적재기', 'base': 'පසුබිම_අගය', 'options': 'අභිරුචි', 'binary': 'ද්විමය', 'args': 'විස්තාරකය_ආරා_ව', 'command': 'විධානය'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
