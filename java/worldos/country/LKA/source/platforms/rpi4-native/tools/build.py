#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/තැනුම_පද්ධතිය.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('තැනුම_පද්ධතිය', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('තැනුම_පද්ධතිය')
    대응 = {'network': 'ජාලය', 'BUILD': 'තැනුම_පෙත', 'ar': 'සංරක්ෂිතය_මෙවලම', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ෆොන්ටය_දත්ත', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'විස්තාරකය_ආරා_ව', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ක්_රමය_පිවිසුම', 'main': 'ක්_රියාත්මක_කරන්න_2', 'objcopy': 'වස්තුව_ගොනුව_පරිවර්තකය', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'සාදන්න_පරිශීලක_ස්ථානය', 'f': 'ගොනුව_පිවිසුම', 'extra': '추가영역', 'exports': 'නිර්යාත_කරන්න_වගුව', 'jobs': '빌드작업', 'run': 'ක්_රියාත්මක_කරන්න_විධානය', 'path': 'මාර්_ගය', 'REPO': '저장소', 'tool': 'මෙවලම්', 'classes': 'පන්තිය_පෙත', 'output': '출력결과', 'samples': '예제들', 'symbol': 'සංකේතය_අගය', 'source': '원본자료', 'name': 'නම', 'build_network': 'සාදන්න_ජාලය_48d29d6d', 'font_info': 'ෆොන්ටය_තතු', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
