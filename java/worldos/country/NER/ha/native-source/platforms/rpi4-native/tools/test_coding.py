#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/코딩시험.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Tafiyar_da', 'elf': '실행파일', 'run': 'gudanar_Umarni', 'name': 'Suna', 'path': 'Hanyar_shiga', 'p': '자료위치', 'ROOT': '기준', 'report': 'amincewa_Rahoto', 'args': 'Tubalin_aiki_TSARI'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
