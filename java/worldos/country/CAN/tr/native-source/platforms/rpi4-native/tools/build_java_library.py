#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/자바라이브러리빌드.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('자바라이브러리빌드')
    eşleme_değer = {'header': 'Başlık_değer', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'yük_veri', 'src': '원본주소', 'run': 'yürütmek_komut', 'build_java_library': '자바라이브러리만들기', 'relative': 'göreli_yol', 'classes': 'Sınıf_yol', 'dist': 'dağıtım_yol', 'archive': 'Arşiv', 'output': 'çıktı', 'root': 'kök_ADRES', 'name': 'İsim', 'jar': '자바꾸러미', 'b': 'SANİYE_değer', 'entries': '항목들'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
