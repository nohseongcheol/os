#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/test_FTP.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_FTP', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('test_FTP')
    eşleme_değer = {'timeout': 'yürütme_ZAMANAŞIMI', 'payload': 'yük_veri', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': 'parça_değer', 'data': 'veri', 'proc': 'Süreç', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Arşiv', 'main': 'çalıştır', 'net_source': 'NET_kaynak', 'temporary': '임시자원', 'static_source': 'statik_kaynak', 'java_source': '자바원문', 'echo': 'yankı_sunucu_girdi', 'ROOT': 'işlem_kök', 'text': 'metin', 'marker': 'işaret', 'EchoFixture': 'yankı_düzen', 'command': 'komut', 'out': 'KR_veri', 'expected': '예상결과', 'server_source': 'sunucu_kaynak', 'shell': 'kabuk', 'upload': 'yükle_Dosyalar', 'transcript': 'döküm', 'port': 'bağlantı_noktası_numarası', 'native': 'yerel_fd019377', 'elf': 'çalıştırılabilir', 'server_udp_port': 'sunucu_veri_birimi_taşımak', 'packed': '묶인자료', 'bridge': 'köprü', 'selector': 'seçici', 'end': 'Bitiş_Ofset', 'e': '보조항목', 'ftp': 'dosya_aktarımı_cxn', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'eş_değer', 'result': 'sonuç', 'unchanged': '보존자료', 'line': 'girdi_satırı', 'server_tcp_port': 'sunucu_akış_taşımak', 'source': '원본자료', 'NetworkBridge': 'köprü_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'almak_belge', 'report': 'doğrulama_Rapor'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
