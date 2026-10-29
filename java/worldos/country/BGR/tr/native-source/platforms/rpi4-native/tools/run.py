#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/yürütmek_komut.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('yürütmek_komut', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('yürütmek_komut')
    eşleme_değer = {'supported': '지원목록', 'parser': 'ayrıştırıcı', 'qemu': '모의기계', 'run_desktop': 'çalıştırma_Masaüstü', 'main': 'çalıştır', 'host': 'konak', 'status': 'Durum_değer', 'NetworkBridge': 'köprü_3de4fe3a', 'ROOT': 'işlem_kök', 'bridge': 'köprü', 'loader': 'yükleyici', 'base': 'Arka_Plan_değer', 'options': 'Seçenekler', 'binary': 'ikili', 'args': 'bağımsız_değişken_DİZİ', 'command': 'komut'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
