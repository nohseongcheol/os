#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/실행파일시험.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('실행파일시험')
    eşleme_değer = {'out': 'KR_veri', 'expected': '예상결과', 'phoff': 'program_Başlık_Ofset', 'offset': 'Ofset_değer', 'invalid': 'geçersiz_veri', 'path': 'yol', 'executable': 'yürütülebilir_RESİM', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'sonuç', 'format_': 'biçim_b87fd068', 'main': 'çalıştır', 'content': 'içerik_değer', 'source': '원본자료', 'name': 'İsim', 'reference': 'Karşılaştırma_temel', 'ROOT': 'işlem_kök', 'value': 'değer', 'report': 'doğrulama_Rapor'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
