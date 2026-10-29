#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/예제빌드.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'fáìlì_Àtòkọ', 'java': '자바실행', 'run': 'ṣiṣẹ́_àṣẹ', 'path': 'ọ̀nà', 'p': '자료위치', 'readme': 'KÀ_MÍ', 'build_java_library': '자바라이브러리만들기', 'code': 'ìtọ́sọ́nà_ÀTẸ̀LÉRA', 'index': '색인', 'classes': 'ọ̀wọ́_ọ̀nà', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Àkóónú_iye', 'source': '원본자료', 'name': 'Orúkọ', 'target': 'àfojúsùn', 'manifest': '꾸러미명세', 'language': 'Èdè'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
