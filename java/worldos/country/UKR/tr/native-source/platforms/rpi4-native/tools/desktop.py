#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/Masaüstü_Görünüm.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Masaüstü_Görünüm', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('Masaüstü_Görünüm')
    eşleme_değer = {'count': 'girdi_BAĞ_DEĞ_SAY', 'special': '특수글쇠', 'error': 'hata', 'exact': 'ÖZDEŞ_değer', 'network': 'ağ', 'closed': 'bilgi_teknolojisi_kapalı', 'length': 'süre_değer', 'opened': '열림', 'ftp_port': 'dosya_aktarımı_bağlantı_noktası_numarası', 'server': 'sunucu_değer', 'resources': 'Kaynaklar', 'data': 'veri', 'shift': 'SHIFT_tuşu', 'send': 'göndermek', 'run_desktop': 'çalıştırma_Masaüstü', 'protocol': 'ağ_ABI', 'forwards': '전달규칙들', 'host': 'konak', 'text': 'metin', 'korean': '한글여부', 'port': 'bağlantı_noktası_numarası', 'signum': '신호번호', 'version': 'sürüm_numarası', 'parser': 'ayrıştırıcı', 'bridge': 'köprü', 'kind': 'alan_değer', 'tail': '끝부분', 'size': 'Boyut', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinat', 'prefix': 'satır_aralığı_parça', 'client': 'istemci', 'char': 'karakter_verileri', 'work': '작업경로', 'Keyboard': 'klavye', 'x': 'x_koordinatı', 'down': '누르는중', 'net': 'köprü_girdi', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'bağımsız_değişken_DİZİ', 'Hangul': '한글조합', 'chunk': 'parça_değer', 'proc': 'Süreç', 'Desktop': 'bağla_Masaüstü', 'buttons': '단추들', 'thread': 'arkaPlanGörevi', 'pressed': '눌림', 'previous': 'Önceki', 'toggle': 'geçiş_mod', 'command': 'komut', 'sock': 'yuva_değer', 'frame': 'yürütme_kare', 'ctrl': 'CTRL', 'path': 'yol', 'cp': 'karakter_kodlaması', 'terminate': 'sonlandırmak', 'security': 'Güvenlik', 'vnc_port': '원격화면접속번호', 'body': 'gövde_metni', 'index': 'ARA_Dizin', 'exited': '종료됨', 'keysym': 'tuş_simge', 'output': 'çıktı', 'keyboard': 'klavye_girdi', 'interrupted': '가로채기됨', 'listener': 'almak_taşımak', 'reader': 'Okuyucu', 'NetworkBridge': 'köprü_3de4fe3a', 'gui': '그림화면', 'worker': 'işleniyor_Görev'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
