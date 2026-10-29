#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/තැනුම_ජාලය.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('තැනුම_ජාලය', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('තැනුම_ජාලය')
    대응 = {'obj': 'ගමනාන්ත_ගොනුව', 'objects': 'ගමනාන්තය_ගොනු', 'library': 'ලේඛාගාරය', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'ගොනුව_ලැයිස්තුව', 'source': '원본자료', 'run': 'ක්_රියාත්මක_කරන්න_විධානය', 'flags': '설정비트', 'path': 'මාර්_ගය', 'build_network': 'සාදන්න_ජාලය_48d29d6d', 'cc': '시언어번역기', 'ar': 'සංරක්ෂිතය_මෙවලම'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
