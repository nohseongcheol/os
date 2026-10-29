#!/usr/bin/env python3
"""기존 yol 호환 giriş_noktası. fiili_veri gerçekleme: ../araçlar/예제되돌림서버.py"""
import importlib as AL_değer
import sys as işletim_sistemi_değer
from pathlib import Path as yol
işletim_sistemi_değer.path.insert(0, str(yol(__file__).resolve().parents[1] / 'araçlar'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    gerçekleme = AL_değer.import_module('예제되돌림서버')
    eşleme_değer = {'data': 'veri', 'sock': 'yuva_değer', 'tcp_port': 'TCP_bağlantı_noktası', 'chunk': 'parça_değer', 'received': '수신됨', 'self': '자신', 'UDP': 'veri_birimi_sap_istek', 'thread': 'arkaPlanGörevi', 'echo': 'yankı_sunucu_girdi', 'TCP': 'sap_cxn_istek', 'EchoServers': 'yankı_Sunucular', 'parser': 'ayrıştırıcı', 'server': 'sunucu_değer', 'udp_port': 'UDP_taşımak', 'args': 'bağımsız_değişken_DİZİ'}
    for Önceki_öğe, geçerli_öğe in eşleme_değer.items():
        if hasattr(gerçekleme, geçerli_öğe): globals()[Önceki_öğe] = getattr(gerçekleme, geçerli_öğe)
