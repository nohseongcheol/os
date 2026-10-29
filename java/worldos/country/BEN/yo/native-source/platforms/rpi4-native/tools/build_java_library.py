#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'àkọlé_iye', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'ojúlówó_détà_détà', 'src': '원본주소', 'run': 'ṣiṣẹ́_àṣẹ', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'ọ̀wọ́_ọ̀nà', 'dist': '배포경로', 'archive': 'Ìpamọ_ọlọ́jọ́pípẹ́', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Orúkọ', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
