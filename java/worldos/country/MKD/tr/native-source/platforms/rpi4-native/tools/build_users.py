#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/BLD_kullanıcı_yer.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_kullanıcı_yer', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('BLD_kullanıcı_yer')
    eşleme_değer = {'mode': 'metot_mod', 'header': 'Başlık_değer', 'i': '순번', 'build_ccompiler': 'açmak_C_derleyici', 'ar': 'Arşiv_araç', 'posix': '포직스경로', 'payload': 'yük_veri', 'flags': 'Yapılandırma_BITS', 'cases': 'test_çalışması', 'cc': 'C_derleyici', 'data': 'veri', 'build_java_library': '자바라이브러리만들기', 'ld': 'bağlayıcı_araç', 'repo': 'depo_yol', 'build_python': 'açmak_PYTHON', 'inc': 'içermek_yol', 'argument': '전달값', 'text': 'metin', 'headers': 'Başlık_Liste', 'cxx': '시플플번역기', 'valid': 'geçerli', 'build': 'BLD', 'build_users': 'açmak_kullanıcı_yer', 'compiler': 'derleyici_araç', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'program_Başlık_Ofset', 'offset': 'Ofset_değer', 'text_address': 'komut_ADRES', 'abi': 'Ara_ABI', 'assembly': 'derleme', 'run': 'yürütmek_komut', 'path': 'yol', 'p': 'veri_konum', 'changed': '바뀐자료', 'n': 'öğe_BAĞ_DEĞ_SAY', 'flag': 'Ayarlar_değer', 'index': 'ARA_Dizin', 'classes': 'Sınıf_yol', 'output': 'çıktı', 'loads': '적재구획', 'data_address': 'veri_ADRES', 'symbol': 'simge_değer', 'root': 'kök_ADRES', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'İsim', 'value': 'değer', 'fmt': 'biçim_932e03c8', 'work': '작업경로'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
