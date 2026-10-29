#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/köprü_3de4fe3a.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('köprü_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('köprü_3de4fe3a')
    eşleme_değer = {'response': 'cevap', 'parts': 'yol_bileşen', 's': 'dize_veri', 'i': '순번', 'close': 'Kapat', 'forward': '전달규칙', 'slip_input': 'Seri_Hat_İnternet_Protokolü_artış', 'self': '자신', 'item': 'girdi_değer', 'flags': 'Yapılandırma_BITS', 'ftp_port': 'dosya_aktarımı_bağlantı_noktası_numarası', 'args': 'bağımsız_değişken_DİZİ', 'server': 'sunucu_değer', 'data': 'veri', 'ethernet_input': 'Ethernet_artış', 'trace_packet': 'iz_paket', 'GATEWAY': 'ağ_geçidi_donanım_ADRES', 'rule': 'kural_değer', 'protocol': 'ağ_ABI', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'konak', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'konuk', 'destination': 'hedef_veri_ADRES', 'ethernet_port': 'Ethernet_bağlantı_noktası', 'b': 'SANİYE_değer', 'MAC': 'mutlak_adres', 'arp': 'ADRES_çözme_paket', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': 'yürütme_kare', 'loop': 'Döngü_değer', 'port': 'bağlantı_noktası_numarası', 'offset': 'Ofset_değer', 'readable': '읽을수있음', 'c': 'kod_noktası', 'p': 'veri_konum', 'writers': '쓰기대상들', 'IP': 'İnternet_adresi_değer', 'e': '보조항목', 'n': 'öğe_BAĞ_DEĞ_SAY', 'packet': 'paket_veri', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'köprü_3de4fe3a', 'window': 'Pencere', 'capture': 'çekmek'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
