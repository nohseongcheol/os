#!/usr/bin/env python3
"""dữLiệuThựcTế RFB 클라이언트로 QEMU 창의 한글/giáTrịPhím/클립보드/마우스와 MànHình 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from khungNhìnMànLàmViệc import giáTrịChínhXác
from thựcThiLệnh import gốcCâyDựÁn


def chạy():
    đầuRa=gốcCâyDựÁn/'build/verification/desktop'; đầuRa.mkdir(parents=True,exist_ok=True)
    tiếnTrình=subprocess.Popen(['python3',str(gốcCâyDựÁn/'CôngCụ/khungNhìnMànLàmViệc.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    bộGiámSátSựSẵnSàng=selectors.DefaultSelector(); bộGiámSátSựSẵnSàng.register(tiếnTrình.stdout,selectors.EVENT_READ)
    bảnGhiDiễnTiến=bytearray(); báoCáoViệcThẩmĐịnh={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest()}
    def đếnKhi(dấuMốc,chạy=0):
        thờiGianHạnChót=time.monotonic()+45
        while dấuMốc not in bảnGhiDiễnTiến[chạy:]:
            if time.monotonic()>thờiGianHạnChót or tiếnTrình.poll() is not None: raise AssertionError(bảnGhiDiễnTiến[chạy:].decode('utf-8','replace'))
            for giáTrịĐãNhấn,_ in bộGiámSátSựSẵnSàng.select(.1):
                DữLiệu=giáTrịĐãNhấn.fileobj.read(4096)
                if DữLiệu: bảnGhiDiễnTiến.extend(DữLiệu)
        return bytes(bảnGhiDiễnTiến[chạy:])
    try:
        đếnKhi(b'TERMINAL READY')
        sốCổng=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',bảnGhiDiễnTiến).group(1))
        with socket.create_connection(('127.0.0.1',sốCổng),timeout=10) as máyKhách:
            assert giáTrịChínhXác(máyKhách,12)==b'RFB 003.008\n'; máyKhách.sendall(b'RFB 003.008\n')
            assert 1 in giáTrịChínhXác(máyKhách,giáTrịChínhXác(máyKhách,1)[0]); máyKhách.sendall(b'\x01'); assert giáTrịChínhXác(máyKhách,4)==b'\0'*4
            máyKhách.sendall(b'\x01'); giáTrịBanĐầu=giáTrịChínhXác(máyKhách,24); assert struct.unpack('>HH',giáTrịBanĐầu[:4])==(640,480); giáTrịChínhXác(máyKhách,struct.unpack('>I',giáTrịBanĐầu[20:])[0])
            máyKhách.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            máyKhách.sendall(struct.pack('>BBHi',2,0,1,0))
            def giáTrịĐãNhấn(giáTrịKýHiệu,làĐangNhấn=True): máyKhách.sendall(struct.pack('>BBHI',4,int(làĐangNhấn),0,giáTrịKýHiệu))
            def kýTựCóKiểu(vănBản):
                for dữLiệuKýTự in vănBản:
                    kýHiệu=0xff0d if dữLiệuKýTự=='\n' else ord(dữLiệuKýTự) if ord(dữLiệuKýTự)<256 else 0x01000000|ord(dữLiệuKýTự)
                    giáTrịĐãNhấn(kýHiệu); giáTrịĐãNhấn(kýHiệu,False)
            def phímNhấn(giáTrịKýHiệu): giáTrịĐãNhấn(giáTrịKýHiệu); giáTrịĐãNhấn(giáTrịKýHiệu,False)
            # Start with English keys only, as delivered without a host IME.
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('echo '); phímNhấn(0xffc6)
            kýTựCóKiểu('dkssudgktpdy gksrmf'); phímNhấn(0xffc6); kýTựCóKiểu('\n')
            đếnKhi('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('echo ')
            giáTrịĐãNhấn(0xffe1); phímNhấn(32); giáTrịĐãNhấn(0xffe1,False)
            kýTựCóKiểu('dlfr'); phímNhấn(0xff08); phímNhấn(0xff08); kýTựCóKiểu('fr')
            phímNhấn(0xff31); kýTựCóKiểu(' EN\n')
            đếnKhi('\r\n읽 EN\r\njkoros-native> '.encode(),giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('echo '); phímNhấn(0xff31)
            kýTựCóKiểu('rhk rkqtk RkRnd'); phímNhấn(0xff31); kýTựCóKiểu('\n')
            đếnKhi('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),giáTrịĐộLệch)
            # The same composition edits UTF-8 text in the native vi editor.
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('vi đầuVàoHangul.txt\n'); đếnKhi(b'NORMAL',giáTrịĐộLệch)
            kýTựCóKiểu('i'); phímNhấn(0xffc6); kýTựCóKiểu('gksrmf dlfr'); phímNhấn(0xffc6)
            phímNhấn(0xff1b); kýTựCóKiểu(':wq\n'); đếnKhi(b'jkoros-native> ',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('cat đầuVàoHangul.txt\n')
            đếnKhi('한글 읽'.encode(),giáTrịĐộLệch); đếnKhi(b'jkoros-native> ',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('help ko\n')
            đếnKhi('한/toánHạngKhôngSố giáTrịPhím, Shift+Space 또는 F9'.encode(),giáTrịĐộLệch); đếnKhi(b'jkoros-native> ',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('clear\necho "VNC 한글 giáTrịVào 😀"\n'); đếnKhi('VNC 한글 giáTrịVào 😀\r\n'.encode(),giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); giáTrịĐãNhấn(0xffe3); giáTrịĐãNhấn(ord('u')); giáTrịĐãNhấn(ord('u'),False); giáTrịĐãNhấn(0xffe3,False); kýTựCóKiểu('echo CONTROL_OK\n'); đếnKhi(b'\r\nCONTROL_OK\r\n',giáTrịĐộLệch)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            giáTrịBảngTạm='echo "giáTrịDán làĐầyĐủ"\n'.encode(); giáTrịĐộLệch=len(bảnGhiDiễnTiến)
            máyKhách.sendall(struct.pack('>B3xI',6,len(giáTrịBảngTạm))+giáTrịBảngTạm)
            for sựKiện,_ in bộGiámSátSựSẵnSàng.select(.15):
                khốiDữLiệu=sựKiện.fileobj.read(4096)
                if khốiDữLiệu: bảnGhiDiễnTiến.extend(khốiDữLiệu)
            assert 'giáTrịDán làĐầyĐủ'.encode() not in bảnGhiDiễnTiến[giáTrịĐộLệch:]
            giáTrịĐãNhấn(0xffe3); giáTrịĐãNhấn(0xffe1); giáTrịĐãNhấn(ord('v')); giáTrịĐãNhấn(ord('v'),False); giáTrịĐãNhấn(0xffe1,False); giáTrịĐãNhấn(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            đếnKhi('\r\n붙여넣기 làĐầyĐủ\r\njkoros-native> '.encode(),giáTrịĐộLệch)
            máyKhách.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            màuRGB=bytearray(640*480*3); cácMụcĐãThấy=False
            while not cácMụcĐãThấy:
                vănBảnThôngBáo=giáTrịChínhXác(máyKhách,1)[0]
                if vănBảnThôngBáo==2: continue
                if vănBảnThôngBáo==3:
                    cỡ=struct.unpack('>I',giáTrịChínhXác(máyKhách,7)[3:])[0]; giáTrịChínhXác(máyKhách,cỡ); continue
                assert vănBảnThôngBáo==0,vănBảnThôngBáo
                danhSáchCácHìnhChữNhật=struct.unpack('>H',giáTrịChínhXác(máyKhách,3)[1:])[0]
                for _ in range(danhSáchCácHìnhChữNhật):
                    tọaĐộX,tọaĐộY,giáTrịRộngĐãYêuCầu,giáTrịCaoĐãYêuCầu,bảngMãKýTự=struct.unpack('>HHHHi',giáTrịChínhXác(máyKhách,12)); assert bảngMãKýTự==0,bảngMãKýTự
                    danhSáchCácĐiểmẢnh=giáTrịChínhXác(máyKhách,giáTrịRộngĐãYêuCầu*giáTrịCaoĐãYêuCầu*4)
                    for thứBậcPhíaTrong in range(giáTrịCaoĐãYêuCầu):
                        for chỉSốThứBậc in range(giáTrịRộngĐãYêuCầu):
                            địaChỉNguyênBản=(thứBậcPhíaTrong*giáTrịRộngĐãYêuCầu+chỉSốThứBậc)*4; địaChỉĐích=((tọaĐộY+thứBậcPhíaTrong)*640+tọaĐộX+chỉSốThứBậc)*3
                            màuRGB[địaChỉĐích:địaChỉĐích+3]=bytes((danhSáchCácĐiểmẢnh[địaChỉNguyênBản+2],danhSáchCácĐiểmẢnh[địaChỉNguyênBản+1],danhSáchCácĐiểmẢnh[địaChỉNguyênBản]))
                    cácMụcĐãThấy=True
            assert màuRGB[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (đầuRa/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+màuRGB)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(màuRGB)).save(str(đầuRa/'vnc-terminal.png'))
            giáTrịĐộLệch=len(bảnGhiDiễnTiến)
            giáTrịĐãNhấn(0xffe3); giáTrịĐãNhấn(0xffe1); giáTrịĐãNhấn(ord('t')); giáTrịĐãNhấn(ord('t'),False); giáTrịĐãNhấn(0xffe1,False); giáTrịĐãNhấn(0xffe3,False)
            đếnKhi(b'TERMINAL FOCUS 2',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('echo SECOND_VNC_WINDOW\n'); đếnKhi(b'\r\nSECOND_VNC_WINDOW\r\n',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); máyKhách.sendall(struct.pack('>BBHH',5,1,576,81)); máyKhách.sendall(struct.pack('>BBHH',5,0,576,81)); đếnKhi(b'TERMINAL FOCUS 1',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('python -c \'print("x"*9000)\'\n'); đếnKhi(b'\r\njkoros-native> ',giáTrịĐộLệch)
            assert len(bảnGhiDiễnTiến)-giáTrịĐộLệch>8192,'exercise output longer than bridge status buffer'
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); máyKhách.sendall(struct.pack('>BBHH',5,1,560,63)); máyKhách.sendall(struct.pack('>BBHH',5,0,560,63)); đếnKhi(b'TERMINAL FOCUS 1',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); máyKhách.sendall(struct.pack('>BBHH',5,1,80,16)); máyKhách.sendall(struct.pack('>BBHH',5,0,80,16)); đếnKhi(b'TERMINAL FOCUS 1',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('echo REOPENED_VNC_WINDOW\n'); đếnKhi(b'\r\nREOPENED_VNC_WINDOW\r\n',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); kýTựCóKiểu('gui\n'); đếnKhi(b'GUI READY:',giáTrịĐộLệch)
            giáTrịĐộLệch=len(bảnGhiDiễnTiến); máyKhách.sendall(struct.pack('>BBHH',5,1,80,332)); máyKhách.sendall(struct.pack('>BBHH',5,0,80,332)); đếnKhi(b'TERMINAL READY',giáTrịĐộLệch)
            báoCáoViệcThẩmĐịnh.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if tiếnTrình.poll() is None:
            tiếnTrình.terminate()
            try: tiếnTrình.wait(timeout=8)
            except subprocess.TimeoutExpired: tiếnTrình.kill(); tiếnTrình.wait()
        bộGiámSátSựSẵnSàng.close(); tiếnTrình.stdout.close()
        (đầuRa/'serial.log').write_bytes(bảnGhiDiễnTiến)
        (đầuRa/'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh,indent=2)+'\n')


if __name__=='__main__': chạy()
