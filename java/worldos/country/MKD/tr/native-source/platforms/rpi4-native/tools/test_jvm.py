#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/test_Java_Sanal_Makinesi.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_Java_Sanal_Makinesi', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('test_Java_Sanal_Makinesi')
    eşleme_değer = {'message': 'uyarı_SMS', 's': 'dize_veri', 'actual': 'fiili_KR', 'match': '일치', 'payload': 'yük_veri', 'cases': 'test_çalışması', 'fixture': 'test_veri', 'main': 'çalıştır', 'ROOT': 'işlem_kök', 'text': 'metin', 'valid': 'geçerli', 'includes': '포함인수', 'include': 'içermek', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Bitenler_tutar', 'classes': 'Sınıf_yol', 'output': 'çıktı', 'result': 'sonuç', 'cmd': '명령인수', 'name': 'İsim', 'jar': '자바꾸러미', 'report': 'doğrulama_Rapor', 'tests': 'test_listesi'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
