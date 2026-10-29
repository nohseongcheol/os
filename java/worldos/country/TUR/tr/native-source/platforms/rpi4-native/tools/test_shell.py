#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/test_kabuk.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_kabuk', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('test_kabuk')
    eşleme_değer = {'timeout': 'yürütme_ZAMANAŞIMI', 'x': 'x_koordinatı', 'msg': 'ağ_belge', 'i': '순번', 'reply': 'yanıt', 'call': '호출', 'args': 'bağımsız_değişken_DİZİ', 'chunk': 'parça_değer', 'data': 'veri', 'proc': 'Süreç', 'long_text': '긴글', 'restored': '복원자료', 'send': 'göndermek', 'file': 'dosya', 'main': 'çalıştır', 'found': 'Ara_KR', 'ROOT': 'işlem_kök', 'text': 'metin', 'marker': 'işaret', 'command': 'komut', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'kabuk', 'poll': '준비살피미', 'transcript': 'döküm', 'end': 'Bitiş_Ofset', 'image': 'RESİM', 'key': '누름값', 'y': 'Y_koordinat', 'output': 'çıktı', 'result': 'sonuç', 'client': 'istemci', 'line': 'girdi_satırı', 'stream': 'akış_değer', 'name': 'İsim', 'value': 'değer', 'receive': 'almak_belge', 'report': 'doğrulama_Rapor', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
