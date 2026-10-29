#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/oluştur.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('oluştur', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('oluştur')
    eşleme_değer = {'network': 'ağ', 'BUILD': 'BLD_yol', 'ar': 'Arşiv_araç', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'yazı_tipi_veri', 'flags': 'Yapılandırma_BITS', 'a': '첫째값', 'cc': 'C_derleyici', 'args': 'bağımsız_değişken_DİZİ', 'source_flags': '원본설정', 'ld': 'bağlayıcı_araç', 'method': 'metot_girdi', 'main': 'çalıştır', 'objcopy': 'nesne_dosyası_dönüştürücü', 'ROOT': 'işlem_kök', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'derleyici_araç', 'build_users': 'açmak_kullanıcı_yer', 'f': 'Dosya_girdi', 'extra': '추가영역', 'exports': 'dışarı_aktarmak_tablo', 'jobs': '빌드작업', 'run': 'yürütmek_komut', 'path': 'yol', 'REPO': 'depo_kök', 'tool': 'araçlar', 'classes': 'Sınıf_yol', 'output': 'çıktı', 'samples': '예제들', 'symbol': 'simge_değer', 'source': '원본자료', 'name': 'İsim', 'build_network': 'açmak_ağ', 'font_info': 'yazı_tipi_bilgi', 'manifest': 'paket_iş_bildirim', 'work': '작업경로'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
