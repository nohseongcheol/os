#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/gudanar_Umarni.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('gudanar_Umarni', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('gudanar_Umarni')
    대응 = {'supported': '지원목록', 'parser': 'tatsar_manhaja', 'qemu': '모의기계', 'run_desktop': 'Gudanar_da_destof', 'main': 'Tafiyar_da', 'host': 'sauka', 'status': 'Matsayi_Daraja', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'Bi_bango_Daraja', 'options': 'Zaɓuɓɓuka', 'binary': 'Mai_bangare_biyu', 'args': 'Tubalin_aiki_TSARI', 'command': 'Umarni'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
