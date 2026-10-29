#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/yükle_Dosyalar.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('yükle_Dosyalar', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('yükle_Dosyalar')
    eşleme_değer = {'data': 'veri', 'i': '순번', 'name': 'İsim', 'c': 'kod_noktası', 'p': 'veri_konum', 'args': 'bağımsız_değişken_DİZİ'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
