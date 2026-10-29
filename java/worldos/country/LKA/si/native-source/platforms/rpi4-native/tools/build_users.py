#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/තැනුම_පරිශීලක_ස්ථානය.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('තැනුම_පරිශීලක_ස්ථානය', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('තැනුම_පරිශීලක_ස්ථානය')
    대응 = {'mode': 'ක්_රමය_ප්_රකාරය', 'header': 'ශීර්ෂය_අගය', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'සංරක්ෂිතය_මෙවලම', 'posix': '포직스경로', 'payload': 'ගෙවීම්_භාරය_දත්ත', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'දත්ත', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'පෙළ', 'headers': 'ශීර්ෂය_ලැයිස්තුව', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'තැනුම', 'build_users': 'සාදන්න_පරිශීලක_ස්ථානය', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'යෙදු_ශීර්ෂය_ඕෆ්සෙට්', 'offset': 'ඕෆ්සෙට්_අගය', 'text_address': 'විධානය_යොමුව', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ක්_රියාත්මක_කරන්න_විධානය', 'path': 'මාර්_ගය', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'පසුතල_අගය', 'index': '색인', 'classes': 'පන්තිය_පෙත', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'දත්ත_යොමුව', 'symbol': 'සංකේතය_අගය', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'නම', 'value': 'අගය', 'fmt': 'හැඩතලය_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
