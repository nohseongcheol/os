#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/되돌림시험서버.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'Tarin_bayani', 'e': '보조항목', 'connection': 'haɗi_e05f319b', 'f': 'Fayil_Mashigar_bayanai', 'peer': 'Fiya_Daraja', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'haɗi_masarrafa', 'EchoFixture': '되돌림시험서버', 'args': 'Tubalin_aiki_TSARI', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
