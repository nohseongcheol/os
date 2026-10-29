#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/dışarı_aktarmak_SDK.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('dışarı_aktarmak_SDK', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('dışarı_aktarmak_SDK')
    eşleme_değer = {'out': 'KR_veri', 'obj': 'hedef_dosya', 'relative': 'göreli_yol', 'compiler_archive': 'derleyici_Arşiv', 'sdk': 'geliştirme_seti', 'dist': 'dağıtım_yol', 'archive': 'Arşiv', 'main': 'çalıştır', 'posix': '포직스경로', 'files': 'dosya_listesi', 'source': '원본자료', 'name': 'İsim', 'target': 'hedef', 'ROOT': 'işlem_kök', 'destination': 'hedef_veri_ADRES', 'manifest': 'paket_iş_bildirim', 'work': '작업경로'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
