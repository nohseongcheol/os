#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/BLD_PYTHON.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_PYTHON', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('BLD_PYTHON')
    eşleme_değer = {'ld': 'bağlayıcı_araç', 'archive': 'Arşiv', 'SHA256': 'doğrulama_özet', 'build_python': 'açmak_PYTHON', 'root': 'kök_ADRES', 'source': '원본자료', 'name': 'İsim', 'path': 'yol', 'VERSION': 'sürüm_değer_237a4c94', 'cc': 'C_derleyici', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'üye'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
