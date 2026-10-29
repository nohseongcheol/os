#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/BLD_ağ.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_ağ', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('BLD_ağ')
    eşleme_değer = {'obj': 'hedef_dosya', 'objects': 'hedef_Dosyalar', 'library': 'kitaplık', 'output': 'çıktı', 'port': 'bağlantı_noktası_numarası', 'root': 'kök_ADRES', 'files': 'dosya_listesi', 'source': '원본자료', 'run': 'yürütmek_komut', 'flags': 'Yapılandırma_BITS', 'path': 'yol', 'build_network': 'açmak_ağ', 'cc': 'C_derleyici', 'ar': 'Arşiv_araç'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
