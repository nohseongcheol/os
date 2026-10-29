#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'දත්ත', 'img': 'චිත්_රය_අගය', 'bits': '비트들', 'x': 'x_ඛණ්ඩාංකය', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'පෙත_ලැයිස්තුව', 'y': '세로좌표', 'main': 'ක්_රියාත්මක_කරන්න_2', 'src': '원본주소', 'fonts': 'ෆොන්ටය_ලැයිස්තුව', 'ROOT': '기준', 'p': '자료위치', 'cp': 'අනුලකුණ_සංකේතනය', 'target': 'ඉලක්කය'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
