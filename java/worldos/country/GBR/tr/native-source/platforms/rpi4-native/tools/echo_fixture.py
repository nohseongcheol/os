#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/yankı_düzen.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('yankı_düzen', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('yankı_düzen')
    eşleme_değer = {'data': 'veri', 'e': '보조항목', 'connection': 'cxn_e05f319b', 'f': 'Dosya_girdi', 'peer': 'eş_değer', 'self': '자신', 'udp': 'veri_birimi_denetim', 't': 'Terminal_girdi', 'tcp': 'cxn_denetim', 'EchoFixture': 'yankı_düzen', 'args': 'bağımsız_değişken_DİZİ', 'chunk': 'parça_değer'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
