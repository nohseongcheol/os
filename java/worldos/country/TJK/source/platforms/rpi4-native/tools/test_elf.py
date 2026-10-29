#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/실행파일시험.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'барнома_Сарнавор_Интиқолшавӣ', 'offset': 'Интиқолшавӣ_қимат', 'invalid': 'беэътибор_иттилоот', 'path': 'масир', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'формат_b87fd068', 'main': 'порча', 'content': 'Мӯҳтаво_қимат', 'source': '원본자료', 'name': 'Ном', 'reference': '비교기준', 'ROOT': '기준', 'value': 'қимат', 'report': 'санҷиши_эътибор_гузориш'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
