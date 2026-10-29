#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Kalit_VALUE 입력은 자체 o_zak_VALUE UART로 전달한다. localhost 전용, 단일 boshqaruv_VALUE 클라이언트.
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
from bajarmoq_buyruq import Buyruq
from local_input import create


def EXACT_VALUE(소켓, Hajmi):
    ma_lumotlar = bytearray()
    while len(ma_lumotlar) < Hajmi:
        조각 = 소켓.recv(Hajmi - len(ma_lumotlar))
        if not 조각: raise EOFError()
        ma_lumotlar.extend(조각)
    return bytes(ma_lumotlar)


class klaviatura:
    def __init__(자신, yuborish, 입력방식알림=None):
        자신.바이트전송 = yuborish; 자신.Ctrl_Shift_va_Alt_klavishalari = set(); 자신.almashish_buferi_VALUE = b''
        자신.한글조합기 = create(yuborish, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Kalit = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def yuborish(자신, ma_lumotlar):
        자신.한글조합기.조합확정()
        자신.바이트전송(ma_lumotlar)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Kalit_ramz):
        if Kalit_ramz in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.Ctrl_Shift_va_Alt_klavishalari.add(Kalit_ramz)
            else: 자신.Ctrl_Shift_va_Alt_klavishalari.discard(Kalit_ramz)
            return
        if not 누르는중:
            자신.SWITCH_Kalit.discard(Kalit_ramz)
            return
        CTRL = bool(자신.Ctrl_Shift_va_Alt_klavishalari & {0xffe3, 0xffe4})
        SHIFT_klavishasi = bool(자신.Ctrl_Shift_va_Alt_klavishalari & {0xffe1, 0xffe2})
        if CTRL and SHIFT_klavishasi and Kalit_ramz in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Kalit_ramz in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.yuborish(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Kalit_ramz==0xff1b: 자신.유니코드입력=None
            elif Kalit_ramz==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Kalit_ramz<128 and chr(Kalit_ramz) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Kalit_ramz)
            return
        if Kalit_ramz in (0xff31,0xffc6) or Kalit_ramz==32 and SHIFT_klavishasi and not CTRL:
            if Kalit_ramz not in 자신.SWITCH_Kalit: 자신.SWITCH_MODE()
            자신.SWITCH_Kalit.add(Kalit_ramz)
            return
        if Kalit_ramz==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_klavishasi and Kalit_ramz in (ord('t'),ord('T')):
            자신.yuborish(bytes([30,2,1,0,0,0,0])); return
        if Kalit_ramz==0xffc3: 자신.yuborish(bytes([30,2,2,0,0,0,0])); return
        if Kalit_ramz==0xffc9: 자신.yuborish(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_klavishasi and Kalit_ramz in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.yuborish(자신.almashish_buferi_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Kalit_ramz in 특수글쇠: 자신.yuborish(특수글쇠[Kalit_ramz]); return
        belgi_kodlash = Kalit_ramz & 0xffffff if Kalit_ramz & 0xff000000 == 0x01000000 else Kalit_ramz
        if belgi_kodlash > 0x10ffff or 0xd800 <= belgi_kodlash <= 0xdfff or Kalit_ramz >= 0xff00 and Kalit_ramz < 0x1000000: return
        if CTRL and 0x40 <= belgi_kodlash <= 0x7f: 자신.yuborish(bytes([belgi_kodlash & 31])); return
        if belgi_kodlash < 32: return
        if 자신.한글여부 and 자신.Ctrl_Shift_va_Alt_klavishalari & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.kanal_Kalit(chr(belgi_kodlash), altgr=True): return
        앞부분 = b'\x1b' if 자신.Ctrl_Shift_va_Alt_klavishalari & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=belgi_kodlash<127:
            belgi_ma_lumotlar=chr(belgi_kodlash).upper() if SHIFT_klavishasi else chr(belgi_kodlash)
            if 자신.한글조합기.kanal_Kalit(belgi_ma_lumotlar): return
        자신.yuborish(앞부분 + chr(belgi_kodlash).encode('utf-8'))


class ulash_ishchi_stol:
    def __init__(자신, Jarayon):
        자신.Jarayon=Jarayon; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def yuborish(자신, ma_lumotlar):
        if not ma_lumotlar or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Jarayon.stdin.write(ma_lumotlar); 자신.Jarayon.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                ma_lumotlar=자신.Jarayon.stdout.read(4096)
                if not ma_lumotlar: break
                sys.stdout.buffer.write(ma_lumotlar); sys.stdout.buffer.flush()
                끝부분=(끝부분+ma_lumotlar)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.yuborish(b'terminal\n')
        finally: 자신.닫힘=True

    def mijoz(자신, mijoz, yo_l):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); mijoz.settimeout(10)
        klaviatura_kiritish=klaviatura(자신.yuborish,lambda 한글여부:자신.yuborish(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(yo_l))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            mijoz.sendall(EXACT_VALUE(server_VALUE,12))
            판번호=EXACT_VALUE(mijoz,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(판번호)
            element_COUNT=EXACT_VALUE(server_VALUE,1);mijoz.sendall(element_COUNT+EXACT_VALUE(server_VALUE,element_COUNT[0]))
            Xavfsizlik=EXACT_VALUE(mijoz,1)
            if Xavfsizlik!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(Xavfsizlik)
            if 판번호==b'RFB 003.008\n':mijoz.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(mijoz,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            mijoz.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            mijoz.settimeout(None);server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        toifa_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if toifa_VALUE==0:
                            머리=EXACT_VALUE(server_VALUE,3);kiritish_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 masofaviy_VALUE 포인터의 중복을 피한다.
                            yashirin_VALUE=포인터지원
                            if yashirin_VALUE:mijoz.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            mijoz.sendall(bytes([toifa_VALUE])+머리)
                            for _ in range(kiritish_COUNT):
                                사각형=EXACT_VALUE(server_VALUE,12);가로,Vertikal_holat,폭,높이,kodlash_VALUE=struct.unpack('>HHHHi',사각형)
                                if kodlash_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodlash_VALUE))
                                mijoz.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    ma_lumotlar=EXACT_VALUE(server_VALUE,min(남음,65536));mijoz.sendall(ma_lumotlar);남음-=len(ma_lumotlar)
                        elif toifa_VALUE==1:
                            머리=EXACT_VALUE(server_VALUE,5);element_COUNT=struct.unpack('>H',머리[3:])[0]
                            mijoz.sendall(bytes([toifa_VALUE])+머리+EXACT_VALUE(server_VALUE,element_COUNT*6))
                        elif toifa_VALUE==2:mijoz.sendall(bytes([toifa_VALUE]))
                        elif toifa_VALUE==3:
                            머리=EXACT_VALUE(server_VALUE,7);element_COUNT=struct.unpack('>I',머리[3:])[0]
                            if element_COUNT>1048576:raise ValueError('server clipboard too large')
                            mijoz.sendall(bytes([toifa_VALUE])+머리+EXACT_VALUE(server_VALUE,element_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(toifa_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:mijoz.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                toifa_VALUE=EXACT_VALUE(mijoz,1)[0]
                if toifa_VALUE==4:
                    asosiy_matn=EXACT_VALUE(mijoz,7); klaviatura_kiritish.누름값(asosiy_matn[0]!=0,struct.unpack('>I',asosiy_matn[3:])[0]); continue
                if toifa_VALUE==255:
                    asosiy_matn=EXACT_VALUE(mijoz,11)
                    if asosiy_matn[0]!=0: raise ValueError('unsupported QEMU input extension')
                    klaviatura_kiritish.누름값(struct.unpack('>H',asosiy_matn[1:3])[0]!=0,struct.unpack('>I',asosiy_matn[3:7])[0]); continue
                if toifa_VALUE==5:
                    asosiy_matn=EXACT_VALUE(mijoz,5); 단추들,x_koordinata,Y_tugmasi_koordinat=struct.unpack('>BHH',asosiy_matn)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: klaviatura_kiritish.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordinata<576 and 112<=Y_tugmasi_koordinat<372:
                        LOOKUP_INDEX=(Y_tugmasi_koordinat-112)//52
                        if (Y_tugmasi_koordinat-112)%52<40 and LOOKUP_INDEX<5: 자신.yuborish(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.yuborish(bytes([30,1,단추들,x_koordinata&255,x_koordinata>>8,Y_tugmasi_koordinat&255,Y_tugmasi_koordinat>>8]))
                    continue
                if toifa_VALUE==6:
                    asosiy_matn=EXACT_VALUE(mijoz,7); uzunlik_VALUE=struct.unpack('>i',asosiy_matn[3:])[0]
                    if abs(uzunlik_VALUE)>65536: raise ValueError('clipboard too large')
                    Matn=EXACT_VALUE(mijoz,abs(uzunlik_VALUE))
                    if uzunlik_VALUE>=0:
                        try: klaviatura_kiritish.almashish_buferi_VALUE=Matn.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: klaviatura_kiritish.almashish_buferi_VALUE=Matn.decode('latin-1').encode('utf-8')
                        klaviatura_kiritish.almashish_buferi_VALUE=klaviatura_kiritish.almashish_buferi_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([toifa_VALUE])+asosiy_matn+Matn); continue
                if toifa_VALUE==0:
                    asosiy_matn=EXACT_VALUE(mijoz,19)
                    if asosiy_matn[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=asosiy_matn[3]//8
                elif toifa_VALUE==2:
                    asosiy_matn=EXACT_VALUE(mijoz,3); kiritish_COUNT=struct.unpack('>H',asosiy_matn[1:])[0]
                    if kiritish_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(kiritish_COUNT)+'i',EXACT_VALUE(mijoz,kiritish_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 sukut_bo_yicha_qiymat Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    asosiy_matn=struct.pack('>BHi',0,1,0)
                elif toifa_VALUE in (3,150): asosiy_matn=EXACT_VALUE(mijoz,9)
                elif toifa_VALUE==248:
                    asosiy_matn=EXACT_VALUE(mijoz,8)
                    if asosiy_matn[7]>64: raise ValueError('fence too large')
                    asosiy_matn+=EXACT_VALUE(mijoz,asosiy_matn[7])
                elif toifa_VALUE==250: asosiy_matn=EXACT_VALUE(mijoz,3)
                elif toifa_VALUE==251:
                    asosiy_matn=EXACT_VALUE(mijoz,7)
                    if asosiy_matn[5]>16: raise ValueError('too many screens')
                    asosiy_matn+=EXACT_VALUE(mijoz,asosiy_matn[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(toifa_VALUE))
                server_VALUE.sendall(bytes([toifa_VALUE])+asosiy_matn)
        except (OSError,EOFError,ValueError) as Xato:
            if str(Xato): print('VNC client:',Xato,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (mijoz,server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def ishlash_ishchi_stol(접속번호=5902, Tarmoq=False, 파일전송접속번호=2121, 전달규칙들=(), ruxsat_VALUE=(640, 480), mehmon_manzil=None, tashkilotchi_manzil='127.0.0.1'):
    with ExitStack() as Resurslar, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        통신다리항목 = None
        if Tarmoq:
            from 통신다리 import 통신다리
            통신다리항목 = Resurslar.enter_context(통신다리(파일전송접속번호, 전달규칙들, mehmon_manzil=mehmon_manzil, tashkilotchi_manzil=tashkilotchi_manzil))
        yo_l=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',접속번호)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if 통신다리항목 and (원격화면접속번호==파일전송접속번호 or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and tashkilotchi==원격화면접속번호 for 통신규약,tashkilotchi,_ in 통신다리항목.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Jarayon=subprocess.Popen(Buyruq(ruxsat_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(yo_l)]+(통신다리항목.전달인수() if 통신다리항목 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            연결다리=ulash_ishchi_stol(Jarayon); o_quvchi=threading.Thread(target=연결다리.직렬입출력,daemon=True); o_quvchi.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if 통신다리항목: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(tashkilotchi_manzil,파일전송접속번호),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Jarayon.poll() is None:
                    try: mijoz,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): mijoz.close(); continue
                    if not yo_l.exists(): mijoz.close(); continue
                    처리작업=threading.Thread(target=연결다리.mijoz,args=(mijoz,yo_l),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                연결다리.닫힘=True
                if 통신다리항목: 통신다리항목.to_xtamoq_hodisa.set()
                if Jarayon.poll() is None:
                    Jarayon.terminate()
                    try: Jarayon.wait(timeout=5)
                    except subprocess.TimeoutExpired: Jarayon.kill(); Jarayon.wait()
                o_quvchi.join(timeout=2); Jarayon.stdin.close(); Jarayon.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if 통신다리항목 and 통신다리항목.Xato: raise RuntimeError('network bridge: '+통신다리항목.Xato)
            return 0 if 가로채기됨 else Jarayon.returncode


if __name__=='__main__':
    from bajarmoq_buyruq import 해상도읽기
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--port',type=int,default=5902)
    parser.add_argument('--resolution',type=해상도읽기,default=(640,480))
    parser.add_argument('--network',action='store_true'); parser.add_argument('--ftp-port',type=int,default=2121)
    parser.add_argument('--forward',action='append',default=[])
    dalil_ARRAY=parser.parse_args()
    if dalil_ARRAY.forward and not dalil_ARRAY.network: parser.error('--forward requires --network')
    raise SystemExit(ishlash_ishchi_stol(dalil_ARRAY.port,Tarmoq=dalil_ARRAY.network,파일전송접속번호=dalil_ARRAY.ftp_port,전달규칙들=dalil_ARRAY.forward,ruxsat_VALUE=dalil_ARRAY.resolution))
