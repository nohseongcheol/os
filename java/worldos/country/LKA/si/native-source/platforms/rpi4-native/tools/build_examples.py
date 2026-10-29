#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/예제빌드.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'ගොනුව_ලැයිස්තුව', 'java': '자바실행', 'run': 'ක්_රියාත්මක_කරන්න_විධානය', 'path': 'මාර්_ගය', 'p': '자료위치', 'readme': 'README_ගොනුව', 'build_java_library': '자바라이브러리만들기', 'code': 'උපදෙස_අනුක්_රමය', 'index': '색인', 'classes': 'පන්තිය_පෙත', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'අන්තර්ගතය_අගය', 'source': '원본자료', 'name': 'නම', 'target': 'ඉලක්කය', 'manifest': '꾸러미명세', 'language': 'භාෂාව'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
