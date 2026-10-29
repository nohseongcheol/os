#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/test_Masaüstü.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_Masaüstü', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('test_Masaüstü')
    eşleme_değer = {'x': 'x_koordinatı', 'typing': '글자입력', 'message': 'uyarı_SMS', 'start': 'çalıştır', 'down': '누르는중', 'exact': 'ÖZDEŞ_değer', 'i': '순번', 'press': 'bas_tuş', 'rectangles': '사각형들', 'sym': 'simge', 'j': '안쪽순번', 'deadline': 'son_tarih_saat', 'proc': 'Süreç', 'data': 'veri', 'main': 'çalıştır', 'w': '너비값', 'init': '초기값', 'block': 'veri_bloğu', 'ROOT': 'işlem_kök', 'text': 'metin', 'marker': 'işaret', 'report': 'doğrulama_Rapor', 'until': '까지', 'clipboard': 'pano_değer', 'dst': 'hedef_ADRES_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'döküm', 'port': 'bağlantı_noktası_numarası', 'offset': 'Ofset_değer', 'h': '높이값', 'src': '원본주소', 'event': 'Olay', 'encoding': 'karakter_kümesi', 'size': 'Boyut', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinat', 'output': 'çıktı', 'symbol': 'simge_değer', 'client': 'istemci', 'char': 'karakter_verileri', 'rgb': '빛삼원색'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
