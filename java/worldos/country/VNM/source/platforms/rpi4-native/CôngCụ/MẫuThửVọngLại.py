"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class MẫuThửVọngLại:
    def __enter__(giáTrịBảnThân):
        giáTrịBảnThân.điềuKhiểnKếtNối = socket.socket(); giáTrịBảnThân.điềuKhiểnKếtNối.bind(('127.0.0.1', 0)); giáTrịBảnThân.điềuKhiểnKếtNối.listen(1)
        giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu.bind(('127.0.0.1', 0))
        giáTrịBảnThân.điềuKhiểnKếtNối.settimeout(30); giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu.settimeout(30)
        giáTrịBảnThân.cổngTCP = giáTrịBảnThân.điềuKhiểnKếtNối.getsockname()[1]; giáTrịBảnThân.cổngUDP = giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu.getsockname()[1]
        giáTrịBảnThân.cácLỗi = []; giáTrịBảnThân.cóĐãNhận = {}
        def điềuKhiểnKếtNối():
            try:
                kếtNối, _ = giáTrịBảnThân.điềuKhiểnKếtNối.accept()
                with kếtNối:
                    kếtNối.settimeout(5); DữLiệu = bytearray()
                    while b'\n' not in DữLiệu:
                        giáTrịĐoạn = kếtNối.recv(512)
                        if not giáTrịĐoạn: raise RuntimeError('TCP EOF before request')
                        DữLiệu.extend(giáTrịĐoạn)
                    giáTrịBảnThân.cóĐãNhận['tcp'] = bytes(DữLiệu); kếtNối.sendall(DữLiệu)
            except Exception as mụcPhụTrợ: giáTrịBảnThân.cácLỗi.append(str(mụcPhụTrợ))
        def điềuKhiểnĐiệnDữLiệu():
            try:
                DữLiệu, giáTrịĐốiTác = giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu.recvfrom(512); giáTrịBảnThân.cóĐãNhận['udp'] = DữLiệu; giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu.sendto(DữLiệu, giáTrịĐốiTác)
            except Exception as mụcPhụTrợ: giáTrịBảnThân.cácLỗi.append(str(mụcPhụTrợ))
        giáTrịBảnThân.cácLuồngChạy = [threading.Thread(target=mụcTệp, daemon=True) for mụcTệp in (điềuKhiểnKếtNối, điềuKhiểnĐiệnDữLiệu)]
        for mụcThiếtBịCuối in giáTrịBảnThân.cácLuồngChạy: mụcThiếtBịCuối.start()
        return giáTrịBảnThân

    def __exit__(giáTrịBảnThân, *mảngĐốiSố):
        giáTrịBảnThân.điềuKhiểnKếtNối.close(); giáTrịBảnThân.điềuKhiểnĐiệnDữLiệu.close()
        for mụcThiếtBịCuối in giáTrịBảnThân.cácLuồngChạy: mụcThiếtBịCuối.join(timeout=1)
