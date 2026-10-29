#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/qurmaq_Terminal_şrift.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('qurmaq_Terminal_şrift', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('qurmaq_Terminal_şrift')
    대응 = {'data': 'verilənlər', 'img': 'rəsm_VALUE', 'bits': 'Fon_Ağıllı_Ötürmə_Xidməti_Siyahı', 'x': 'x_koordinatı', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'yol_Siyahı', 'y': 'Y_koordinat', 'main': 'İcra_Et', 'src': '원본주소', 'fonts': 'şrift_Siyahı', 'ROOT': 'Project_kök', 'p': 'verilənlər_yerinə_qoymaq', 'cp': 'simvol_kodlaşdırma', 'target': 'hədəf'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
