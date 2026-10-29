#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/코딩시험.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('코딩시험')
    eşleme_değer = {'out': 'KR_veri', 'expected': '예상결과', 'sdk': 'geliştirme_seti', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'çalıştır', 'elf': 'çalıştırılabilir', 'run': 'yürütmek_komut', 'name': 'İsim', 'path': 'yol', 'p': 'veri_konum', 'ROOT': 'işlem_kök', 'report': 'doğrulama_Rapor', 'args': 'bağımsız_değişken_DİZİ'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
