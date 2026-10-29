#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/BLD_Terminal_yazı_tipi.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_Terminal_yazı_tipi', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('BLD_Terminal_yazı_tipi')
    eşleme_değer = {'data': 'veri', 'img': 'çizim_değer', 'bits': 'BITS_Liste', 'x': 'x_koordinatı', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'yol_Liste', 'y': 'Y_koordinat', 'main': 'çalıştır', 'src': '원본주소', 'fonts': 'yazı_tipi_Liste', 'ROOT': 'işlem_kök', 'p': 'veri_konum', 'cp': 'karakter_kodlaması', 'target': 'hedef'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
