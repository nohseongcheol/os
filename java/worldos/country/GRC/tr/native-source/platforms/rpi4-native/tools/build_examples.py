#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/예제빌드.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('예제빌드')
    eşleme_değer = {'out': 'KR_veri', 'build_examples': '예제만들기', 'files': 'dosya_listesi', 'java': '자바실행', 'run': 'yürütmek_komut', 'path': 'yol', 'p': 'veri_konum', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'ARA_Dizin', 'classes': 'Sınıf_yol', 'repo': 'depo_yol', 'root': 'kök_ADRES', 'content': 'içerik_değer', 'source': '원본자료', 'name': 'İsim', 'target': 'hedef', 'manifest': 'paket_iş_bildirim', 'language': 'Dil'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
