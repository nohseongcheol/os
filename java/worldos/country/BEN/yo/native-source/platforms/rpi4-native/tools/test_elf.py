#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/실행파일시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'àtòjọ_ètò_àkọlé_Ìtayọ', 'offset': 'Ìtayọ_iye', 'invalid': 'aláìbẹgbẹmu_détà', 'path': 'ọ̀nà', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'ìgúnrégé_b87fd068', 'main': 'Rọ́ọ̀nù', 'content': 'Àkóónú_iye', 'source': '원본자료', 'name': 'Orúkọ', 'reference': '비교기준', 'ROOT': '기준', 'value': 'iye', 'report': 'Àfọwọ́sí_ìjábọ̀'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
