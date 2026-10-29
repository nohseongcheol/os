#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'ශීර්ෂය_අගය', 'sources': '원문목록', 'i': '순번', 'info': 'පද්ධති_තොරතුරු', 'payload': 'ගෙවීම්_භාරය_දත්ත', 'src': '원본주소', 'run': 'ක්_රියාත්මක_කරන්න_විධානය', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'පන්තිය_පෙත', 'dist': '배포경로', 'archive': 'සංරක්ෂිතය', 'output': '출력결과', 'root': '뿌리주소', 'name': 'නම', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
