#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/BLD_C_derleyici.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_C_derleyici', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('BLD_C_derleyici')
    eşleme_değer = {'out': 'KR_veri', 'builtins': '내장연산', 'header': 'Başlık_değer', 'sdk': 'geliştirme_seti', 'build_ccompiler': 'açmak_C_derleyici', 'i': '순번', 'elf': 'çalıştırılabilir', 'run': 'yürütmek_komut', 'flags': 'Yapılandırma_BITS', 'path': 'yol', 'p': 'veri_konum', 'cc': 'C_derleyici', 'obj': 'hedef_dosya', 'flag': 'Ayarlar_değer', 'ld': 'bağlayıcı_araç', 'objects': 'hedef_Dosyalar', 'repo': 'depo_yol', 'v': '임시값', 'upstream': 'yukarı_akış', 'root': 'kök_ADRES', 'assets': '탑재자료', 'source': '원본자료', 'name': 'İsim', 'includes': '포함인수'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
