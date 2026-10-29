#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/lodawa_Fayiloli.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('lodawa_Fayiloli', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('lodawa_Fayiloli')
    대응 = {'data': 'Tarin_bayani', 'i': '순번', 'name': 'Suna', 'c': 'Lambar_sirrin_harafi', 'p': '자료위치', 'args': 'Tubalin_aiki_TSARI'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
