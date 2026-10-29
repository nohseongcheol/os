#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'иттилоот', 'img': 'нақша_қимат', 'bits': '비트들', 'x': 'координатаи_х', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'масир_Рӯйхат', 'y': '세로좌표', 'main': 'порча', 'src': '원본주소', 'fonts': 'шрифт_Рӯйхат', 'ROOT': '기준', 'p': '자료위치', 'cp': 'аломат_рамзгузорӣ', 'target': 'ҳадаф'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
