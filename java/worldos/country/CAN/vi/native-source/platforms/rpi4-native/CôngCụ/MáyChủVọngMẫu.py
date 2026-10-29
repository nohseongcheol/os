#!/usr/bin/env python3
"""tiếngViệt 네트워크 예제용 Chủ TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class CácMáyChủVọngLại:
    def __init__(giáTrịBảnThân,cổngTCP=0,cổngUDP=0):
        giáTrịBảnThân.cóĐãNhận=[];giáTrịBảnThân.cácLuồngChạy=[]
        cóĐãNhận=giáTrịBảnThân.cóĐãNhận
        class yêuCầuKếtNốiThẻXửLý(socketserver.BaseRequestHandler):
            def handle(giáTrịBảnThân):
                giáTrịBảnThân.request.settimeout(5);DữLiệu=bytearray()
                while b'\n' not in DữLiệu and len(DữLiệu)<=512:
                    giáTrịĐoạn=giáTrịBảnThân.request.recv(512)
                    if not giáTrịĐoạn:return
                    DữLiệu.extend(giáTrịĐoạn)
                cóĐãNhận.append(('tcp',bytes(DữLiệu)));giáTrịBảnThân.request.sendall(DữLiệu)
        class yêuCầuThẻXửLýĐiệnDữLiệu(socketserver.BaseRequestHandler):
            def handle(giáTrịBảnThân):
                DữLiệu,giáTrịỔCắmMạng=giáTrịBảnThân.request;cóĐãNhận.append(('udp',DữLiệu));giáTrịỔCắmMạng.sendto(DữLiệu,giáTrịBảnThân.client_address)
        giáTrịBảnThân.điềuKhiểnKếtNối=socketserver.ThreadingTCPServer(('127.0.0.1',cổngTCP),yêuCầuKếtNốiThẻXửLý)
        try:giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu=socketserver.ThreadingUDPServer(('127.0.0.1',cổngUDP),yêuCầuThẻXửLýĐiệnDữLiệu)
        except Exception:giáTrịBảnThân.điềuKhiểnKếtNối.server_close();raise
        giáTrịBảnThân.điềuKhiểnKếtNối.daemon_threads=giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu.daemon_threads=True
        giáTrịBảnThân.cổngTCP=giáTrịBảnThân.điềuKhiểnKếtNối.server_address[1];giáTrịBảnThân.cổngUDP=giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu.server_address[1]

    def __enter__(giáTrịBảnThân):
        for giáTrịMáyChủ in (giáTrịBảnThân.điềuKhiểnKếtNối,giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu):
            bộLàmViệc=threading.Thread(target=giáTrịMáyChủ.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            bộLàmViệc.start();giáTrịBảnThân.cácLuồngChạy.append(bộLàmViệc)
        return giáTrịBảnThân

    def __exit__(giáTrịBảnThân,*mảngĐốiSố):
        for giáTrịMáyChủ in (giáTrịBảnThân.điềuKhiểnKếtNối,giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu):giáTrịMáyChủ.shutdown();giáTrịMáyChủ.server_close()
        for bộLàmViệc in giáTrịBảnThân.cácLuồngChạy:bộLàmViệc.join(timeout=1)


if __name__=='__main__':
    bộPhânTích=argparse.ArgumentParser(description=__doc__)
    bộPhânTích.add_argument('--tcp-port',type=int,default=9000);bộPhânTích.add_argument('--udp-port',type=int,default=9001)
    mảngĐốiSố=bộPhânTích.parse_args()
    with CácMáyChủVọngLại(mảngĐốiSố.tcp_port,mảngĐốiSố.udp_port) as mụcMáyChủVọngLại:
        print('Chủ TCP {}, UDP {} chuẩnBị. 게스트 địaChỉ: 10.0.2.2. chươngTrìnhRa: Ctrl+C'.format(mụcMáyChủVọngLại.cổngTCP,mụcMáyChủVọngLại.cổngUDP),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
