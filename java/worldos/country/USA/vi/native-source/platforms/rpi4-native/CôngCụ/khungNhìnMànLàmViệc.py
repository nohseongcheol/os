#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, giáTrịPhím 입력은 tựThân giáTrịNhân UART로 전달한다. localhost 전용, 단일 giáTrịĐiềuKhiển 클라이언트.
RFB 3.8: https://www.rfc-editor.org/rfc/rfc6143.html
"""
import argparse
from contextlib import ExitStack
from pathlib import Path
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from thựcThiLệnh import lệnh
from local_input import create


def giáTrịChínhXác(giáTrịỔCắmMạng, cỡ):
    DữLiệu = bytearray()
    while len(DữLiệu) < cỡ:
        giáTrịĐoạn = giáTrịỔCắmMạng.recv(cỡ - len(DữLiệu))
        if not giáTrịĐoạn: raise EOFError()
        DữLiệu.extend(giáTrịĐoạn)
    return bytes(DữLiệu)


class BànPhím:
    def __init__(giáTrịBảnThân, gửi, đãĐổiChếĐộ=None):
        giáTrịBảnThân.cácByteChuyểnGiao = gửi; giáTrịBảnThân.phímBộBổNghĩa = set(); giáTrịBảnThân.giáTrịBảngTạm = b''
        giáTrịBảnThân.BộGhépHangul = create(gửi, Path(__file__).resolve().parents[1]); giáTrịBảnThân.tiếngHàn = False; giáTrịBảnThân.phímChuyển = set()
        giáTrịBảnThân.đầuVàoUnicode = None
        giáTrịBảnThân.đãĐổiChếĐộ = đãĐổiChếĐộ
        if đãĐổiChếĐộ: đãĐổiChếĐộ(False)

    def gửi(giáTrịBảnThân, DữLiệu):
        giáTrịBảnThân.BộGhépHangul.phépGhépChốt()
        giáTrịBảnThân.cácByteChuyểnGiao(DữLiệu)

    def chếĐộChuyển(giáTrịBảnThân):
        giáTrịBảnThân.BộGhépHangul.phépGhépChốt(); giáTrịBảnThân.tiếngHàn = not giáTrịBảnThân.tiếngHàn
        if giáTrịBảnThân.đãĐổiChếĐộ: giáTrịBảnThân.đãĐổiChếĐộ(giáTrịBảnThân.tiếngHàn)

    def giáTrịĐãNhấn(giáTrịBảnThân, làĐangNhấn, kýHiệuPhím):
        if kýHiệuPhím in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if làĐangNhấn: giáTrịBảnThân.phímBộBổNghĩa.add(kýHiệuPhím)
            else: giáTrịBảnThân.phímBộBổNghĩa.discard(kýHiệuPhím)
            return
        if not làĐangNhấn:
            giáTrịBảnThân.phímChuyển.discard(kýHiệuPhím)
            return
        phímĐiềuKhiển = bool(giáTrịBảnThân.phímBộBổNghĩa & {0xffe3, 0xffe4})
        phímDịch = bool(giáTrịBảnThân.phímBộBổNghĩa & {0xffe1, 0xffe2})
        if phímĐiềuKhiển and phímDịch and kýHiệuPhím in (ord('u'),ord('U')):
            giáTrịBảnThân.BộGhépHangul.phépGhépChốt(); giáTrịBảnThân.đầuVàoUnicode = ''; return
        if giáTrịBảnThân.đầuVàoUnicode is not None:
            if kýHiệuPhím in (32,0xff0d):
                try:
                    giáTrị=int(giáTrịBảnThân.đầuVàoUnicode,16)
                    if 32<=giáTrị<=0x10ffff and not 0xd800<=giáTrị<=0xdfff: giáTrịBảnThân.gửi(chr(giáTrị).encode('utf-8'))
                except ValueError: pass
                giáTrịBảnThân.đầuVàoUnicode=None
            elif kýHiệuPhím==0xff1b: giáTrịBảnThân.đầuVàoUnicode=None
            elif kýHiệuPhím==0xff08: giáTrịBảnThân.đầuVàoUnicode=giáTrịBảnThân.đầuVàoUnicode[:-1]
            elif kýHiệuPhím<128 and chr(kýHiệuPhím) in '0123456789abcdefABCDEF' and len(giáTrịBảnThân.đầuVàoUnicode)<6: giáTrịBảnThân.đầuVàoUnicode+=chr(kýHiệuPhím)
            return
        if kýHiệuPhím in (0xff31,0xffc6) or kýHiệuPhím==32 and phímDịch and not phímĐiềuKhiển:
            if kýHiệuPhím not in giáTrịBảnThân.phímChuyển: giáTrịBảnThân.chếĐộChuyển()
            giáTrịBảnThân.phímChuyển.add(kýHiệuPhím)
            return
        if kýHiệuPhím==0xff08 and giáTrịBảnThân.tiếngHàn and not phímĐiềuKhiển and giáTrịBảnThân.BộGhépHangul.xóaLùi(): return
        if phímĐiềuKhiển and phímDịch and kýHiệuPhím in (ord('t'),ord('T')):
            giáTrịBảnThân.gửi(bytes([30,2,1,0,0,0,0])); return
        if kýHiệuPhím==0xffc3: giáTrịBảnThân.gửi(bytes([30,2,2,0,0,0,0])); return
        if kýHiệuPhím==0xffc9: giáTrịBảnThân.gửi(bytes([30,2,3,0,0,0,0])); return
        if phímĐiềuKhiển and phímDịch and kýHiệuPhím in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            giáTrịBảnThân.gửi(giáTrịBảnThân.giáTrịBảngTạm); return
        phímĐặcBiệt = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if kýHiệuPhím in phímĐặcBiệt: giáTrịBảnThân.gửi(phímĐặcBiệt[kýHiệuPhím]); return
        mãHóaKýTự = kýHiệuPhím & 0xffffff if kýHiệuPhím & 0xff000000 == 0x01000000 else kýHiệuPhím
        if mãHóaKýTự > 0x10ffff or 0xd800 <= mãHóaKýTự <= 0xdfff or kýHiệuPhím >= 0xff00 and kýHiệuPhím < 0x1000000: return
        if phímĐiềuKhiển and 0x40 <= mãHóaKýTự <= 0x7f: giáTrịBảnThân.gửi(bytes([mãHóaKýTự & 31])); return
        if mãHóaKýTự < 32: return
        if giáTrịBảnThân.tiếngHàn and giáTrịBảnThân.phímBộBổNghĩa & {0xffea,0xfe03,0xff7e} and not phímĐiềuKhiển and hasattr(giáTrịBảnThân.BộGhépHangul, 'profile'):
            if giáTrịBảnThân.BộGhépHangul.phímCấp(chr(mãHóaKýTự), altgr=True): return
        phầnDẫnĐầu = b'\x1b' if giáTrịBảnThân.phímBộBổNghĩa & {0xffe9, 0xffea} else b''
        if giáTrịBảnThân.tiếngHàn and not phímĐiềuKhiển and not phầnDẫnĐầu and 32<=mãHóaKýTự<127:
            dữLiệuKýTự=chr(mãHóaKýTự).upper() if phímDịch else chr(mãHóaKýTự)
            if giáTrịBảnThân.BộGhépHangul.phímCấp(dữLiệuKýTự): return
        giáTrịBảnThân.gửi(phầnDẫnĐầu + chr(mãHóaKýTự).encode('utf-8'))


class kếtNốiMànLàmViệc:
    def __init__(giáTrịBảnThân, tiếnTrình):
        giáTrịBảnThân.tiếnTrình=tiếnTrình; giáTrịBảnThân.giáTrịKhóa=threading.Lock(); giáTrịBảnThân.đầyĐủSựChuẩnBị=False; giáTrịBảnThân.thiếtBịCuối=False; giáTrịBảnThân.mànHìnhBanĐầu=False; giáTrịBảnThân.làĐãĐóng=False

    def gửi(giáTrịBảnThân, DữLiệu):
        if not DữLiệu or giáTrịBảnThân.làĐãĐóng: return
        with giáTrịBảnThân.giáTrịKhóa:
            try: giáTrịBảnThân.tiếnTrình.stdin.write(DữLiệu); giáTrịBảnThân.tiếnTrình.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def vàoRaNốiTiếp(giáTrịBảnThân):
        phầnPhầnKết=b''
        try:
            while True:
                DữLiệu=giáTrịBảnThân.tiếnTrình.stdout.read(4096)
                if not DữLiệu: break
                sys.stdout.buffer.write(DữLiệu); sys.stdout.buffer.flush()
                phầnPhầnKết=(phầnPhầnKết+DữLiệu)[-8192:]
                đãMở=phầnPhầnKết.rfind(b'TERMINAL READY'); làĐãĐóng=phầnPhầnKết.rfind(b'TERMINAL CLOSED'); mànHìnhBảnVẽ=phầnPhầnKết.rfind(b'GUI READY:'); cóĐãRa=phầnPhầnKết.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(đãMở,làĐãĐóng,mànHìnhBảnVẽ,cóĐãRa)>=0:
                    giáTrịBảnThân.thiếtBịCuối=đãMở>max(làĐãĐóng,mànHìnhBảnVẽ,cóĐãRa)
                    giáTrịBảnThân.mànHìnhBanĐầu=mànHìnhBảnVẽ>max(đãMở,làĐãĐóng,cóĐãRa)
                if not giáTrịBảnThân.đầyĐủSựChuẩnBị and b'jkoros-native> ' in phầnPhầnKết:
                    giáTrịBảnThân.đầyĐủSựChuẩnBị=True; giáTrịBảnThân.gửi(b'terminal\n')
        finally: giáTrịBảnThân.làĐãĐóng=True

    def máyKhách(giáTrịBảnThân, máyKhách, đườngDẫn):
        giáTrịMáyChủ=socket.socket(socket.AF_UNIX); giáTrịMáyChủ.settimeout(10); máyKhách.settimeout(10)
        mụcBànPhím=BànPhím(giáTrịBảnThân.gửi,lambda tiếngHàn:giáTrịBảnThân.gửi(bytes([30,3,int(tiếngHàn),0,0,0,0])))
        cácNútTrướcĐó=0
        try:
            giáTrịMáyChủ.connect(str(đườngDẫn))
            # trạngTháiBanĐầu 협상은 순서대로 끝낸다. giáTrịSau ĐầuRa 가닥만 클라이언트에 쓴다.
            máyKhách.sendall(giáTrịChínhXác(giáTrịMáyChủ,12))
            sốPhiênBản=giáTrịChínhXác(máyKhách,12)
            if sốPhiênBản not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            giáTrịMáyChủ.sendall(sốPhiênBản)
            sốLượngPhầnMục=giáTrịChínhXác(giáTrịMáyChủ,1);máyKhách.sendall(sốLượngPhầnMục+giáTrịChínhXác(giáTrịMáyChủ,sốLượngPhầnMục[0]))
            bảoMật=giáTrịChínhXác(máyKhách,1)
            if bảoMật!=b'\x01': raise ValueError('unexpected security type')
            giáTrịMáyChủ.sendall(bảoMật)
            if sốPhiênBản==b'RFB 003.008\n':máyKhách.sendall(giáTrịChínhXác(giáTrịMáyChủ,4))
            giáTrịMáyChủ.sendall(giáTrịChínhXác(máyKhách,1))
            giáTrịBanĐầu=giáTrịChínhXác(giáTrịMáyChủ,24)
            máyKhách.sendall(giáTrịBanĐầu+giáTrịChínhXác(giáTrịMáyChủ,struct.unpack('>I',giáTrịBanĐầu[20:])[0]))
            cácByteĐiểmẢnh=giáTrịBanĐầu[4]//8;đượcHỗTrợConTrỏ=False
            máyKhách.settimeout(None);giáTrịMáyChủ.settimeout(None)
            def đầuRa():
                try:
                    while True:
                        giáTrịLoạiMục=giáTrịChínhXác(giáTrịMáyChủ,1)[0]
                        if giáTrịLoạiMục==0:
                            giáTrịĐầu=giáTrịChínhXác(giáTrịMáyChủ,3);sốLượngMục=struct.unpack('>H',giáTrịĐầu[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 giáTrịTừXa 포인터의 중복을 피한다.
                            giáTrịẨn=đượcHỗTrợConTrỏ
                            if giáTrịẨn:máyKhách.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            máyKhách.sendall(bytes([giáTrịLoạiMục])+giáTrịĐầu)
                            for _ in range(sốLượngMục):
                                hìnhChữNhật=giáTrịChínhXác(giáTrịMáyChủ,12);vịTríNgang,vịTríDọc,khoảngTrảiRộng,giáTrịCao,giáTrịBảngMã=struct.unpack('>HHHHi',hìnhChữNhật)
                                if giáTrịBảngMã!=0:raise ValueError('unexpected framebuffer encoding: '+str(giáTrịBảngMã))
                                máyKhách.sendall(hìnhChữNhật)
                                dữLiệuSốDư=khoảngTrảiRộng*giáTrịCao*cácByteĐiểmẢnh
                                while dữLiệuSốDư:
                                    DữLiệu=giáTrịChínhXác(giáTrịMáyChủ,min(dữLiệuSốDư,65536));máyKhách.sendall(DữLiệu);dữLiệuSốDư-=len(DữLiệu)
                        elif giáTrịLoạiMục==1:
                            giáTrịĐầu=giáTrịChínhXác(giáTrịMáyChủ,5);sốLượngPhầnMục=struct.unpack('>H',giáTrịĐầu[3:])[0]
                            máyKhách.sendall(bytes([giáTrịLoạiMục])+giáTrịĐầu+giáTrịChínhXác(giáTrịMáyChủ,sốLượngPhầnMục*6))
                        elif giáTrịLoạiMục==2:máyKhách.sendall(bytes([giáTrịLoạiMục]))
                        elif giáTrịLoạiMục==3:
                            giáTrịĐầu=giáTrịChínhXác(giáTrịMáyChủ,7);sốLượngPhầnMục=struct.unpack('>I',giáTrịĐầu[3:])[0]
                            if sốLượngPhầnMục>1048576:raise ValueError('server clipboard too large')
                            máyKhách.sendall(bytes([giáTrịLoạiMục])+giáTrịĐầu+giáTrịChínhXác(giáTrịMáyChủ,sốLượngPhầnMục))
                        else:raise ValueError('unexpected RFB server message: '+str(giáTrịLoạiMục))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:máyKhách.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            bộLàmViệc=threading.Thread(target=đầuRa,daemon=True);bộLàmViệc.start()
            while not giáTrịBảnThân.làĐãĐóng:
                giáTrịLoạiMục=giáTrịChínhXác(máyKhách,1)[0]
                if giáTrịLoạiMục==4:
                    vănBảnThân=giáTrịChínhXác(máyKhách,7); mụcBànPhím.giáTrịĐãNhấn(vănBảnThân[0]!=0,struct.unpack('>I',vănBảnThân[3:])[0]); continue
                if giáTrịLoạiMục==255:
                    vănBảnThân=giáTrịChínhXác(máyKhách,11)
                    if vănBảnThân[0]!=0: raise ValueError('unsupported QEMU input extension')
                    mụcBànPhím.giáTrịĐãNhấn(struct.unpack('>H',vănBảnThân[1:3])[0]!=0,struct.unpack('>I',vănBảnThân[3:7])[0]); continue
                if giáTrịLoạiMục==5:
                    vănBảnThân=giáTrịChínhXác(máyKhách,5); cácNút,tọaĐộX,tọaĐộY=struct.unpack('>BHH',vănBảnThân)
                    làĐãNhấn=cácNút&~cácNútTrướcĐó; cácNútTrướcĐó=cácNút
                    if làĐãNhấn: mụcBànPhím.BộGhépHangul.phépGhépChốt()
                    if làĐãNhấn&1 and giáTrịBảnThân.mànHìnhBanĐầu and 64<=tọaĐộX<576 and 112<=tọaĐộY<372:
                        chỉSốTraCứu=(tọaĐộY-112)//52
                        if (tọaĐộY-112)%52<40 and chỉSốTraCứu<5: giáTrịBảnThân.gửi(bytes([ord('1')+chỉSốTraCứu]))
                    else: giáTrịBảnThân.gửi(bytes([30,1,cácNút,tọaĐộX&255,tọaĐộX>>8,tọaĐộY&255,tọaĐộY>>8]))
                    continue
                if giáTrịLoạiMục==6:
                    vănBảnThân=giáTrịChínhXác(máyKhách,7); độDài=struct.unpack('>i',vănBảnThân[3:])[0]
                    if abs(độDài)>65536: raise ValueError('clipboard too large')
                    vănBản=giáTrịChínhXác(máyKhách,abs(độDài))
                    if độDài>=0:
                        try: mụcBànPhím.giáTrịBảngTạm=vănBản.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: mụcBànPhím.giáTrịBảngTạm=vănBản.decode('latin-1').encode('utf-8')
                        mụcBànPhím.giáTrịBảngTạm=mụcBànPhím.giáTrịBảngTạm[:65536].decode('utf-8','ignore').encode('utf-8')
                    giáTrịMáyChủ.sendall(bytes([giáTrịLoạiMục])+vănBảnThân+vănBản); continue
                if giáTrịLoạiMục==0:
                    vănBảnThân=giáTrịChínhXác(máyKhách,19)
                    if vănBảnThân[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    cácByteĐiểmẢnh=vănBảnThân[3]//8
                elif giáTrịLoạiMục==2:
                    vănBảnThân=giáTrịChínhXác(máyKhách,3); sốLượngMục=struct.unpack('>H',vănBảnThân[1:])[0]
                    if sốLượngMục>512: raise ValueError('too many encodings')
                    cácGiáTrịĐãMãHóa=struct.unpack('>'+str(sốLượngMục)+'i',giáTrịChínhXác(máyKhách,sốLượngMục*4))
                    đượcHỗTrợConTrỏ=-239 in cácGiáTrịĐãMãHóa
                    # 로컬 MànHình 중계는 giáTrịMặcĐịnh Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    vănBảnThân=struct.pack('>BHi',0,1,0)
                elif giáTrịLoạiMục in (3,150): vănBảnThân=giáTrịChínhXác(máyKhách,9)
                elif giáTrịLoạiMục==248:
                    vănBảnThân=giáTrịChínhXác(máyKhách,8)
                    if vănBảnThân[7]>64: raise ValueError('fence too large')
                    vănBảnThân+=giáTrịChínhXác(máyKhách,vănBảnThân[7])
                elif giáTrịLoạiMục==250: vănBảnThân=giáTrịChínhXác(máyKhách,3)
                elif giáTrịLoạiMục==251:
                    vănBảnThân=giáTrịChínhXác(máyKhách,7)
                    if vănBảnThân[5]>16: raise ValueError('too many screens')
                    vănBảnThân+=giáTrịChínhXác(máyKhách,vănBảnThân[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(giáTrịLoạiMục))
                giáTrịMáyChủ.sendall(bytes([giáTrịLoạiMục])+vănBảnThân)
        except (OSError,EOFError,ValueError) as lỗi:
            if str(lỗi): print('VNC client:',lỗi,file=sys.stderr,flush=True)
        finally:
            for giáTrịỔCắmMạng in (máyKhách,giáTrịMáyChủ):
                try: giáTrịỔCắmMạng.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                giáTrịỔCắmMạng.close()


def chạyMànLàmViệc(sốCổng=5902, mạng=False, sốCổngChuyểnGiaoTệp=2121, cácQuyTắcViệcChuyểnTiếp=(), giáTrịĐộPhânGiải=(640, 480), địaChỉKhách=None, địaChỉChủ='127.0.0.1'):
    with ExitStack() as cácTàiNguyên, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as đườngDẫnĐangLàmViệc:
        mụcCầuNốiMạng = None
        if mạng:
            from cầuNốiMạng import cầuNốiMạng
            mụcCầuNốiMạng = cácTàiNguyên.enter_context(cầuNốiMạng(sốCổngChuyểnGiaoTệp, cácQuyTắcViệcChuyểnTiếp, địaChỉKhách=địaChỉKhách, địaChỉChủ=địaChỉChủ))
        đườngDẫn=Path(đườngDẫnĐangLàmViệc)/'display.sock'
        with socket.socket() as nhậnCổng:
            nhậnCổng.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            nhậnCổng.bind(('127.0.0.1',sốCổng)); nhậnCổng.listen(1); nhậnCổng.settimeout(.2)
            cổngVNC=nhậnCổng.getsockname()[1]
            if mụcCầuNốiMạng and (cổngVNC==sốCổngChuyểnGiaoTệp or 50000<=cổngVNC<=50007 or any(ABIMạng=='tcp' and Chủ==cổngVNC for ABIMạng,Chủ,_ in mụcCầuNốiMạng.cácQuyTắcViệcChuyểnTiếp)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            tiếnTrình=subprocess.Popen(lệnh(giáTrịĐộPhânGiải)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(đườngDẫn)]+(mụcCầuNốiMạng.đốiSốĐãChuyểnTiếp() if mụcCầuNốiMạng else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            cầuNối=kếtNốiMànLàmViệc(tiếnTrình); bộĐọc=threading.Thread(target=cầuNối.vàoRaNốiTiếp,daemon=True); bộĐọc.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(nhậnCổng.getsockname()[1]),flush=True)
            if mụcCầuNốiMạng: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(địaChỉChủ,sốCổngChuyểnGiaoTệp),flush=True)
            def chấmDứt(sốTínHiệu,khungViệcThựcThi): raise KeyboardInterrupt()
            trướcĐó=signal.signal(signal.SIGTERM,chấmDứt)
            tácVụViệcXửLý=None; đãBịNgắt=False
            try:
                while tiếnTrình.poll() is None:
                    try: máyKhách,_=nhậnCổng.accept()
                    except socket.timeout: continue
                    if tácVụViệcXửLý is not None and tácVụViệcXửLý.is_alive(): máyKhách.close(); continue
                    if not đườngDẫn.exists(): máyKhách.close(); continue
                    tácVụViệcXửLý=threading.Thread(target=cầuNối.máyKhách,args=(máyKhách,đườngDẫn),daemon=True); tácVụViệcXửLý.start()
            except KeyboardInterrupt: đãBịNgắt=True
            finally:
                cầuNối.làĐãĐóng=True
                if mụcCầuNốiMạng: mụcCầuNốiMạng.sựKiệnTạmDừng.set()
                if tiếnTrình.poll() is None:
                    tiếnTrình.terminate()
                    try: tiếnTrình.wait(timeout=5)
                    except subprocess.TimeoutExpired: tiếnTrình.kill(); tiếnTrình.wait()
                bộĐọc.join(timeout=2); tiếnTrình.stdin.close(); tiếnTrình.stdout.close(); signal.signal(signal.SIGTERM,trướcĐó)
            if mụcCầuNốiMạng and mụcCầuNốiMạng.lỗi: raise RuntimeError('network bridge: '+mụcCầuNốiMạng.lỗi)
            return 0 if đãBịNgắt else tiếnTrình.returncode


if __name__=='__main__':
    from thựcThiLệnh import đọcĐộPhânGiải
    bộPhânTích=argparse.ArgumentParser(description=__doc__); bộPhânTích.add_argument('--port',type=int,default=5902)
    bộPhânTích.add_argument('--resolution',type=đọcĐộPhânGiải,default=(640,480))
    bộPhânTích.add_argument('--network',action='store_true'); bộPhânTích.add_argument('--ftp-port',type=int,default=2121)
    bộPhânTích.add_argument('--forward',action='append',default=[])
    mảngĐốiSố=bộPhânTích.parse_args()
    if mảngĐốiSố.forward and not mảngĐốiSố.network: bộPhânTích.error('--forward requires --network')
    raise SystemExit(chạyMànLàmViệc(mảngĐốiSố.port,mạng=mảngĐốiSố.network,sốCổngChuyểnGiaoTệp=mảngĐốiSố.ftp_port,cácQuyTắcViệcChuyểnTiếp=mảngĐốiSố.forward,giáTrịĐộPhânGiải=mảngĐốiSố.resolution))
