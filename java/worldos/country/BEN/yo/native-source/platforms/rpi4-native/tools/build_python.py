#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/파이썬빌드.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파이썬빌드')
    대응 = {'ld': '연결편집기', 'archive': 'Ìpamọ_ọlọ́jọ́pípẹ́', 'SHA256': 'Àfọwọ́sí_burú', 'build_python': '파이썬만들기', 'root': '뿌리주소', 'source': '원본자료', 'name': 'Orúkọ', 'path': 'ọ̀nà', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'ọmọ_ẹgbẹ́'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
