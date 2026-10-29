#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/부팅시험.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('부팅시험')
    eşleme_değer = {'timeout': 'yürütme_ZAMANAŞIMI', 'response': 'cevap', 'msg': 'ağ_belge', 'exact': 'ÖZDEŞ_değer', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Çalıştır', 'cancel': 'İptal_işlem', 'cmd_byte': 'komut_bayt', 'reply': 'yanıt', 'points': '지점들', 'server': 'sunucu_değer', 'data': 'veri', 'prompt': 'istem', 'enter': 'girmek', 'imported': '들여온파일', 'send': 'göndermek', 'main': 'çalıştır', 'ROOT': 'işlem_kök', 'text': 'metin', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': 'yükle_Dosyalar', 'pixels_file': 'piksel_Dosya', 'pixels_data': 'piksel_veri', 'edit': 'Düzenle_değer', 'receive_until': '표시까지받기', 'selector': 'seçici', 'size': 'Boyut', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SANİYE_GUI', 'y': 'Y_koordinat', 'result': 'sonuç', 'samples': '예제들', 'client': 'istemci', 'line': 'girdi_satırı', 'report': 'doğrulama_Rapor', 'work': '작업경로', 'x': 'x_koordinatı', 'python_checks': '파이썬검사', 'download': 'indir', 'greeting': '인사', 'dims': '치수', 'chunk': 'parça_değer', 'deadline': 'son_tarih_saat', 'proc': 'Süreç', 'content': 'içerik_değer', 'block': 'veri_bloğu', 'marker': 'işaret', 'command': 'komut', 'expected': '예상결과', 'shell': 'kabuk', 'drawing': 'çizim_yol', 'f': 'Dosya_girdi', 'transcript': 'döküm', 'offset': 'Ofset_değer', 'path': 'yol', 'screenshot': 'ekran_kırpması', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'çıktı', 'stream': 'akış_değer', 'cmd': '명령인수', 'name': 'İsim', 'qmp': '모의제어접속'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
