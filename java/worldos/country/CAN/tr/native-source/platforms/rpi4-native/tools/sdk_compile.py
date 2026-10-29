#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/SDK_derlemek.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('SDK_derlemek', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('SDK_derlemek')
    eşleme_değer = {'compiler': 'derleyici_araç', 'obj': 'hedef_dosya', 'sdk': 'geliştirme_seti', 'output': 'çıktı', 'main': 'çalıştır', 'elf': 'çalıştırılabilir', 'is_c': 'bilgi_teknolojisi_C_Dil', 'parser': 'ayrıştırıcı', 'language': 'Dil', 'work': '작업경로', 'args': 'bağımsız_değişken_DİZİ'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
