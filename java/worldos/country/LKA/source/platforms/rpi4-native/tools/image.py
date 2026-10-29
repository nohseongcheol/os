#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/සාදන්න_අනුරුව.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('සාදන්න_අනුරුව', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('සාදන්න_අනුරුව')
    대응 = {'total': '총량', 'start': 'ක්_රියාත්මක_කරන්න_2', 'firmware': '기초제어프로그램', 'files': 'ගොනුව_ලැයිස්තුව', 'archive_base': '압축기준', 'partition': 'පංගුව_ගොනුව', 'archive': 'සංරක්ෂිතය', 'main': 'ක්_රියාත්මක_කරන්න_2', 'block': 'දත්ත_අවහිර_කරන්න', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'අදියර_අගය', 'out': '결과자료', 'expected': '예상결과', 'f': 'ගොනුව_පිවිසුම', 'src': '원본주소', 'path': 'මාර්_ගය', 'p': '자료위치', 'extracted': '추출자료', 'member': 'සාමාජිකයා', 'mbr': '주부트기록', 'image': 'අනුරුව', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'වරපත', 'source': '원본자료', 'name': 'නම', 'value': 'අගය', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
