#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/자바가상기계시험.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'අනුලකුණු_වැල_දත්ත', 'actual': '실제결과', 'match': '일치', 'payload': 'ගෙවීම්_භාරය_දත්ත', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ක්_රියාත්මක_කරන්න_2', 'ROOT': '기준', 'text': 'පෙළ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'පන්තිය_පෙත', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'නම', 'jar': '자바꾸러미', 'report': 'වලංගුකරණය_වාර්තාව', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
