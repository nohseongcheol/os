#!/usr/bin/env python3
"""Türkçe 네트워크 예제용 konak TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class yankı_Sunucular:
    def __init__(자신,TCP_bağlantı_noktası=0,UDP_taşımak=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class sap_cxn_istek(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);veri=bytearray()
                while b'\n' not in veri and len(veri)<=512:
                    parça_değer=자신.request.recv(512)
                    if not parça_değer:return
                    veri.extend(parça_değer)
                수신됨.append(('tcp',bytes(veri)));자신.request.sendall(veri)
        class veri_birimi_sap_istek(socketserver.BaseRequestHandler):
            def handle(자신):
                veri,yuva_değer=자신.request;수신됨.append(('udp',veri));yuva_değer.sendto(veri,자신.client_address)
        자신.cxn_denetim=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_bağlantı_noktası),sap_cxn_istek)
        try:자신.veri_birimi_denetim=socketserver.ThreadingUDPServer(('127.0.0.1',UDP_taşımak),veri_birimi_sap_istek)
        except Exception:자신.cxn_denetim.server_close();raise
        자신.cxn_denetim.daemon_threads=자신.veri_birimi_denetim.daemon_threads=True
        자신.TCP_bağlantı_noktası=자신.cxn_denetim.server_address[1];자신.UDP_taşımak=자신.veri_birimi_denetim.server_address[1]

    def __enter__(자신):
        for sunucu_değer in (자신.cxn_denetim,자신.veri_birimi_denetim):
            arkaPlanGörevi=threading.Thread(target=sunucu_değer.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            arkaPlanGörevi.start();자신.작업가닥들.append(arkaPlanGörevi)
        return 자신

    def __exit__(자신,*bağımsız_değişken_DİZİ):
        for sunucu_değer in (자신.cxn_denetim,자신.veri_birimi_denetim):sunucu_değer.shutdown();sunucu_değer.server_close()
        for arkaPlanGörevi in 자신.작업가닥들:arkaPlanGörevi.join(timeout=1)


if __name__=='__main__':
    ayrıştırıcı=argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı.add_argument('--tcp-port',type=int,default=9000);ayrıştırıcı.add_argument('--udp-port',type=int,default=9001)
    bağımsız_değişken_DİZİ=ayrıştırıcı.parse_args()
    with yankı_Sunucular(bağımsız_değişken_DİZİ.tcp_port,bağımsız_değişken_DİZİ.udp_port) as yankı_sunucu_girdi:
        print('konak TCP {}, UDP {} Hazırlan. 게스트 ADRES: 10.0.2.2. Çıkış_program: Ctrl+C'.format(yankı_sunucu_girdi.TCP_bağlantı_noktası,yankı_sunucu_girdi.UDP_taşımak),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
