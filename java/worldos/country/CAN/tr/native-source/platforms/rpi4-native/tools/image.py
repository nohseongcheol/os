#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/açmak_RESİM.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('açmak_RESİM', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('açmak_RESİM')
    eşleme_değer = {'total': 'toplam_kapasite', 'start': 'çalıştır', 'firmware': 'üretici_yazılımı_değer', 'files': 'dosya_listesi', 'archive_base': 'Arşiv_TABAN', 'partition': 'bölüm_Dosya', 'archive': 'Arşiv', 'main': 'çalıştır', 'block': 'veri_bloğu', 'ROOT': 'işlem_kök', 'boot': '부팅경로', 'stage': 'aşama_değer', 'out': 'KR_veri', 'expected': '예상결과', 'f': 'Dosya_girdi', 'src': '원본주소', 'path': 'yol', 'p': 'veri_konum', 'extracted': '추출자료', 'member': 'üye', 'mbr': 'ana_önyükleme_kaydı', 'image': 'RESİM', 'sector_count': '섹터개수', 'dist': 'dağıtım_yol', 'sha': '해시계산', 'license_': 'lisans', 'source': '원본자료', 'name': 'İsim', 'value': 'değer', 'manifest': 'paket_iş_bildirim', 'dest': 'hedef_değer_konum', 'work': '작업경로'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
