#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/yürütmek_Dosya.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('yürütmek_Dosya', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('yürütmek_Dosya')
    eşleme_değer = {'timeout': 'yürütme_ZAMANAŞIMI', 's': 'dize_veri', 'i': '순번', 'match': '일치', 'files': 'dosya_listesi', 'program': 'program', 'executable': 'yürütülebilir_RESİM', 'args': 'bağımsız_değişken_DİZİ', 'chunk': 'parça_değer', 'data': 'veri', 'proc': 'Süreç', 'send': 'göndermek', 'main': 'çalıştır', 'marker': 'işaret', 'command': 'komut', 'include': 'içermek', 'dumped': '갈무리자료', 'run': 'yürütmek_komut', 'p': 'veri_konum', 'parser': 'ayrıştırıcı', 'options': 'Seçenekler', 'kind': 'alan_değer', 'selector': 'seçici', 'upload_data': 'yükle_veri', 'end': 'Bitiş_Ofset', 'n': 'öğe_BAĞ_DEĞ_SAY', 'd': 'hedef_veri', 'key': '누름값', 'output': 'çıktı', 'line': 'girdi_satırı', 'name': 'İsim', 'upload_name': 'yükle_ad', 'receive': 'almak_belge'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
