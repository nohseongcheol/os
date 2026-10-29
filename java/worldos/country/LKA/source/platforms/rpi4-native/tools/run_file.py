#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/ක්_රියාත්මක_කරන්න_ගොනුව.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('ක්_රියාත්මක_කරන්න_ගොනුව', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ක්_රියාත්මක_කරන්න_ගොනුව')
    대응 = {'timeout': '시간제한', 's': 'අනුලකුණු_වැල_දත්ත', 'i': '순번', 'match': '일치', 'files': 'ගොනුව_ලැයිස්තුව', 'program': 'යෙදු', 'executable': '실행가능파일', 'args': 'විස්තාරකය_ආරා_ව', 'chunk': '조각', 'data': 'දත්ත', 'proc': 'සැකසුම', 'send': 'ඊමේල්', 'main': 'ක්_රියාත්මක_කරන්න_2', 'marker': '확인표시', 'command': 'විධානය', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ක්_රියාත්මක_කරන්න_විධානය', 'p': '자료위치', 'parser': '인수해석기', 'options': 'අභිරුචි', 'kind': 'ප්_රවර්ගය_අගය', 'selector': 'වරකය', 'upload_data': 'උඩුගත_කරන්න_දත්ත', 'end': 'නිමා_කරන්න_ඕෆ්සෙට්', 'n': '개수', 'd': 'ගමනාන්තය_දත්ත', 'key': '누름값', 'output': '출력결과', 'line': 'පේළිය', 'name': 'නම', 'upload_name': 'උඩුගත_කරන්න_නම', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
