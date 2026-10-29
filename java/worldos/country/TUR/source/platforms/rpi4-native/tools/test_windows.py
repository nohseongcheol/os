#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/test_Windows.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_Windows', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('test_Windows')
    eşleme_değer = {'wait': '기다리기', 'x': 'x_koordinatı', 's': 'dize_veri', 'xy': 'koordinat_çifti', 'sel': 'seçici_a916db4e', 'seconds': '초단위', 'log': 'LOG_KAYIT', 'at': 'geçerli_konum', 'send': 'göndermek', 'main': 'çalıştır', 'req': 'istek_değer', 'hot': 'kısayol_değer', 'pump': 'sap_olay', 'ROOT': 'işlem_kök', 'marker': 'işaret', 'b': 'SANİYE_değer', 'command': 'komut', 'shell': 'kabuk', 'f': 'Dosya_girdi', 'color': '색상', 'click': 'tık_düğme', 'k': '셋째순번', 'c': 'kod_noktası', 'r': '반환값', 'p': 'veri_konum', 'done': 'Bitenler_tutar', 'end': 'Bitiş_Ofset', 'command_mode': 'komut_mod', 'key': '누름값', 'y': 'Y_koordinat', 'pixels': '화소들', 'result': 'sonuç', 'report': 'doğrulama_Rapor', 'dest': 'hedef_değer_konum', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
