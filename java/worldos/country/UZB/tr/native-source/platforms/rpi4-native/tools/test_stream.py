#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/test_akış.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_akış', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('test_akış')
    eşleme_değer = {'out': 'KR_veri', 'main': 'çalıştır', 'ROOT': 'işlem_kök', 'p': 'veri_konum', 'text': 'metin', 'report': 'doğrulama_Rapor'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
