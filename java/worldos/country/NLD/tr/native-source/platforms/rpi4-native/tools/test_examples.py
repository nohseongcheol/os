#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/예제시험.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('예제시험')
    eşleme_değer = {'count': 'girdi_BAĞ_DEĞ_SAY', 'exact': 'ÖZDEŞ_değer', 'expected_file': '예상파일', 'ftp_port': 'dosya_aktarımı_bağlantı_noktası_numarası', 'data': 'veri', 'graphics_command': 'grafik_komut', 'main': 'çalıştır', 'row': 'SATIR_konum', 'init': '초기값', 'target': 'hedef', 'ROOT': 'işlem_kök', 'text': 'metin', 'binary': 'ikili', 'out': 'KR_veri', 'entry': 'giriş_noktası', 'got': 'GETİRİ_BAĞ_DEĞ_SAY', 'port': 'bağlantı_noktası_numarası', 'graphics_start': 'Start_çizim', 'col': 'SÜTUN_konum', 'begin': 'Start_Ofset', 'kind': 'alan_değer', 'selector': 'seçici', 'n': 'öğe_BAĞ_DEĞ_SAY', 'key': '누름값', 'y': 'Y_koordinat', 'client': 'istemci', 'line': 'girdi_satırı', 'report': 'doğrulama_Rapor', 'language': 'Dil', 'x': 'x_koordinatı', 'start': 'çalıştır', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'göndermek_Liste', 'payload': 'yük_veri', 'proc': 'Süreç', 'w': '너비값', 'temporary': '임시자원', 'echo': 'yankı_sunucu_girdi', 'label': 'ad_tablo', 'content': 'içerik_değer', 'argument': '전달값', 'EchoServers': 'yankı_Sunucular', 'marker': 'işaret', 'expected': '예상결과', 'test_language': 'test_Dil', 'filename': 'Dosya_girdi_ad', 'shell': 'kabuk', 'color': '색상', 'transcript': 'döküm', 'offset': 'Ofset_değer', 'h': '높이값', 'run': 'yürütmek_komut', 'c': 'kod_noktası', 'path': 'yol', 'encoding': 'karakter_kümesi', 'end': 'Bitiş_Ofset', 'ftp': 'dosya_aktarımı_cxn', 'pixels': '화소들', 'symbol': 'simge_değer', 'source': '원본자료', 'name': 'İsim', 'receive': 'almak_belge', 'manifest': 'paket_iş_bildirim'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
