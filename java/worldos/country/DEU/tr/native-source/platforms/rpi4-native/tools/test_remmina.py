#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/원격한글시험.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('원격한글시험')
    eşleme_değer = {'wait': '기다리기', 'typing': '글자입력', 'start': 'çalıştır', 'profile': 'Profil', 'focused': 'Odaklanmış', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'sunucu_değer', 'log': 'LOG_KAYIT', 'args': 'bağımsız_değişken_DİZİ', 'deadline': 'son_tarih_saat', 'data': 'veri', 'candidate': 'aday', 'logs': '기록들', 'kw': 'adlandırılmış_bağımsız_değişken', 'number': '수치', 'main': 'çalıştır', 'ready': '준비완료', 'found': 'Ara_KR', 'guest': 'konuk', 'ROOT': 'işlem_kök', 'marker': 'işaret', 'text': 'metin', 'out': 'KR_veri', 'env': 'ortam', 'f': 'Dosya_girdi', 'port': 'bağlantı_noktası_numarası', 'offset': 'Ofset_değer', 'version': 'sürüm_numarası', 'p': 'veri_konum', 'selector': 'seçici', 'xvfb': 'sanal_monitör', 'display': 'monitör', 'n': 'öğe_BAĞ_DEĞ_SAY', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'sanal_artış_araç', 'name': 'İsim', 'window': 'Pencere', 'report': 'doğrulama_Rapor', 'work': '작업경로'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
