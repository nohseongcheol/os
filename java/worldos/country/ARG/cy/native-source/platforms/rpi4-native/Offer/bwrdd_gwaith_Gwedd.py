#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, bysell_VALUE 입력은 자체 cnewyllyn_VALUE UART로 전달한다. localhost 전용, 단일 rheoli_VALUE 클라이언트.
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
from Gweithredu_gorchymyn import Gorchymyn
from local_input import create


def EXACT_VALUE(소켓, Maint):
    data = bytearray()
    while len(data) < Maint:
        조각 = 소켓.recv(Maint - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class allweddell:
    def __init__(자신, anfon, 입력방식알림=None):
        자신.바이트전송 = anfon; 자신.bysell_addasu = set(); 자신.clipfwrdd_VALUE = b''
        자신.한글조합기 = create(anfon, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.newid_bysell = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def anfon(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def newid_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, bysell_symbol):
        if bysell_symbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.bysell_addasu.add(bysell_symbol)
            else: 자신.bysell_addasu.discard(bysell_symbol)
            return
        if not 누르는중:
            자신.newid_bysell.discard(bysell_symbol)
            return
        CTRL = bool(자신.bysell_addasu & {0xffe3, 0xffe4})
        bysell_SHIFT = bool(자신.bysell_addasu & {0xffe1, 0xffe2})
        if CTRL and bysell_SHIFT and bysell_symbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if bysell_symbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.anfon(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif bysell_symbol==0xff1b: 자신.유니코드입력=None
            elif bysell_symbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif bysell_symbol<128 and chr(bysell_symbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(bysell_symbol)
            return
        if bysell_symbol in (0xff31,0xffc6) or bysell_symbol==32 and bysell_SHIFT and not CTRL:
            if bysell_symbol not in 자신.newid_bysell: 자신.newid_MODE()
            자신.newid_bysell.add(bysell_symbol)
            return
        if bysell_symbol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and bysell_SHIFT and bysell_symbol in (ord('t'),ord('T')):
            자신.anfon(bytes([30,2,1,0,0,0,0])); return
        if bysell_symbol==0xffc3: 자신.anfon(bytes([30,2,2,0,0,0,0])); return
        if bysell_symbol==0xffc9: 자신.anfon(bytes([30,2,3,0,0,0,0])); return
        if CTRL and bysell_SHIFT and bysell_symbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.anfon(자신.clipfwrdd_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if bysell_symbol in 특수글쇠: 자신.anfon(특수글쇠[bysell_symbol]); return
        nod_amgodio = bysell_symbol & 0xffffff if bysell_symbol & 0xff000000 == 0x01000000 else bysell_symbol
        if nod_amgodio > 0x10ffff or 0xd800 <= nod_amgodio <= 0xdfff or bysell_symbol >= 0xff00 and bysell_symbol < 0x1000000: return
        if CTRL and 0x40 <= nod_amgodio <= 0x7f: 자신.anfon(bytes([nod_amgodio & 31])); return
        if nod_amgodio < 32: return
        if 자신.한글여부 and 자신.bysell_addasu & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.ffrwd_bysell(chr(nod_amgodio), altgr=True): return
        앞부분 = b'\x1b' if 자신.bysell_addasu & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=nod_amgodio<127:
            nod_data=chr(nod_amgodio).upper() if bysell_SHIFT else chr(nod_amgodio)
            if 자신.한글조합기.ffrwd_bysell(nod_data): return
        자신.anfon(앞부분 + chr(nod_amgodio).encode('utf-8'))


class Cysylltu_bwrdd_gwaith:
    def __init__(자신, Proses):
        자신.Proses=Proses; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Terfynell=False; 자신.시작화면=False; 자신.닫힘=False

    def anfon(자신, data):
        if not data or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Proses.stdin.write(data); 자신.Proses.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Proses.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terfynell=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.anfon(b'terminal\n')
        finally: 자신.닫힘=True

    def cleient(자신, cleient, LLWYBR):
        gweinydd_VALUE=socket.socket(socket.AF_UNIX); gweinydd_VALUE.settimeout(10); cleient.settimeout(10)
        allweddell_cofnod=allweddell(자신.anfon,lambda 한글여부:자신.anfon(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            gweinydd_VALUE.connect(str(LLWYBR))
            # 초기 협상은 순서대로 끝낸다. 이후 Allbwn 가닥만 클라이언트에 쓴다.
            cleient.sendall(EXACT_VALUE(gweinydd_VALUE,12))
            rhif_fersiwn=EXACT_VALUE(cleient,12)
            if rhif_fersiwn not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            gweinydd_VALUE.sendall(rhif_fersiwn)
            eitem_COUNT=EXACT_VALUE(gweinydd_VALUE,1);cleient.sendall(eitem_COUNT+EXACT_VALUE(gweinydd_VALUE,eitem_COUNT[0]))
            Diogelwch=EXACT_VALUE(cleient,1)
            if Diogelwch!=b'\x01': raise ValueError('unexpected security type')
            gweinydd_VALUE.sendall(Diogelwch)
            if rhif_fersiwn==b'RFB 003.008\n':cleient.sendall(EXACT_VALUE(gweinydd_VALUE,4))
            gweinydd_VALUE.sendall(EXACT_VALUE(cleient,1))
            초기값=EXACT_VALUE(gweinydd_VALUE,24)
            cleient.sendall(초기값+EXACT_VALUE(gweinydd_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            cleient.settimeout(None);gweinydd_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        ardal_VALUE=EXACT_VALUE(gweinydd_VALUE,1)[0]
                        if ardal_VALUE==0:
                            머리=EXACT_VALUE(gweinydd_VALUE,3);cofnod_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 pell_VALUE 포인터의 중복을 피한다.
                            cudd_VALUE=포인터지원
                            if cudd_VALUE:cleient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            cleient.sendall(bytes([ardal_VALUE])+머리)
                            for _ in range(cofnod_COUNT):
                                사각형=EXACT_VALUE(gweinydd_VALUE,12);가로,Ar_i_fyny_safle,폭,높이,amgodio_VALUE=struct.unpack('>HHHHi',사각형)
                                if amgodio_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(amgodio_VALUE))
                                cleient.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EXACT_VALUE(gweinydd_VALUE,min(남음,65536));cleient.sendall(data);남음-=len(data)
                        elif ardal_VALUE==1:
                            머리=EXACT_VALUE(gweinydd_VALUE,5);eitem_COUNT=struct.unpack('>H',머리[3:])[0]
                            cleient.sendall(bytes([ardal_VALUE])+머리+EXACT_VALUE(gweinydd_VALUE,eitem_COUNT*6))
                        elif ardal_VALUE==2:cleient.sendall(bytes([ardal_VALUE]))
                        elif ardal_VALUE==3:
                            머리=EXACT_VALUE(gweinydd_VALUE,7);eitem_COUNT=struct.unpack('>I',머리[3:])[0]
                            if eitem_COUNT>1048576:raise ValueError('server clipboard too large')
                            cleient.sendall(bytes([ardal_VALUE])+머리+EXACT_VALUE(gweinydd_VALUE,eitem_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(ardal_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:cleient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                ardal_VALUE=EXACT_VALUE(cleient,1)[0]
                if ardal_VALUE==4:
                    corff_y_testun=EXACT_VALUE(cleient,7); allweddell_cofnod.누름값(corff_y_testun[0]!=0,struct.unpack('>I',corff_y_testun[3:])[0]); continue
                if ardal_VALUE==255:
                    corff_y_testun=EXACT_VALUE(cleient,11)
                    if corff_y_testun[0]!=0: raise ValueError('unsupported QEMU input extension')
                    allweddell_cofnod.누름값(struct.unpack('>H',corff_y_testun[1:3])[0]!=0,struct.unpack('>I',corff_y_testun[3:7])[0]); continue
                if ardal_VALUE==5:
                    corff_y_testun=EXACT_VALUE(cleient,5); 단추들,cyfesuryn_x,Y_cyfesuryn=struct.unpack('>BHH',corff_y_testun)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: allweddell_cofnod.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=cyfesuryn_x<576 and 112<=Y_cyfesuryn<372:
                        LOOKUP_INDEX=(Y_cyfesuryn-112)//52
                        if (Y_cyfesuryn-112)%52<40 and LOOKUP_INDEX<5: 자신.anfon(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.anfon(bytes([30,1,단추들,cyfesuryn_x&255,cyfesuryn_x>>8,Y_cyfesuryn&255,Y_cyfesuryn>>8]))
                    continue
                if ardal_VALUE==6:
                    corff_y_testun=EXACT_VALUE(cleient,7); hyd_VALUE=struct.unpack('>i',corff_y_testun[3:])[0]
                    if abs(hyd_VALUE)>65536: raise ValueError('clipboard too large')
                    Testun=EXACT_VALUE(cleient,abs(hyd_VALUE))
                    if hyd_VALUE>=0:
                        try: allweddell_cofnod.clipfwrdd_VALUE=Testun.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: allweddell_cofnod.clipfwrdd_VALUE=Testun.decode('latin-1').encode('utf-8')
                        allweddell_cofnod.clipfwrdd_VALUE=allweddell_cofnod.clipfwrdd_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    gweinydd_VALUE.sendall(bytes([ardal_VALUE])+corff_y_testun+Testun); continue
                if ardal_VALUE==0:
                    corff_y_testun=EXACT_VALUE(cleient,19)
                    if corff_y_testun[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=corff_y_testun[3]//8
                elif ardal_VALUE==2:
                    corff_y_testun=EXACT_VALUE(cleient,3); cofnod_COUNT=struct.unpack('>H',corff_y_testun[1:])[0]
                    if cofnod_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(cofnod_COUNT)+'i',EXACT_VALUE(cleient,cofnod_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 gwerth_diofyn Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    corff_y_testun=struct.pack('>BHi',0,1,0)
                elif ardal_VALUE in (3,150): corff_y_testun=EXACT_VALUE(cleient,9)
                elif ardal_VALUE==248:
                    corff_y_testun=EXACT_VALUE(cleient,8)
                    if corff_y_testun[7]>64: raise ValueError('fence too large')
                    corff_y_testun+=EXACT_VALUE(cleient,corff_y_testun[7])
                elif ardal_VALUE==250: corff_y_testun=EXACT_VALUE(cleient,3)
                elif ardal_VALUE==251:
                    corff_y_testun=EXACT_VALUE(cleient,7)
                    if corff_y_testun[5]>16: raise ValueError('too many screens')
                    corff_y_testun+=EXACT_VALUE(cleient,corff_y_testun[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(ardal_VALUE))
                gweinydd_VALUE.sendall(bytes([ardal_VALUE])+corff_y_testun)
        except (OSError,EOFError,ValueError) as Gwall:
            if str(Gwall): print('VNC client:',Gwall,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (cleient,gweinydd_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def rhedeg_bwrdd_gwaith(rhif_porth=5902, Rhwydwaith=False, ffeil_trosglwyddo_rhif_porth=2121, 전달규칙들=(), cydraniad_VALUE=(640, 480), gwestai_ADDRESS=None, lletya_ADDRESS='127.0.0.1'):
    with ExitStack() as Adnoddau, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Rhwydwaith_pont_cofnod = None
        if Rhwydwaith:
            from Rhwydwaith_pont import Rhwydwaith_pont
            Rhwydwaith_pont_cofnod = Adnoddau.enter_context(Rhwydwaith_pont(ffeil_trosglwyddo_rhif_porth, 전달규칙들, gwestai_ADDRESS=gwestai_ADDRESS, lletya_ADDRESS=lletya_ADDRESS))
        LLWYBR=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',rhif_porth)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Rhwydwaith_pont_cofnod and (원격화면접속번호==ffeil_trosglwyddo_rhif_porth or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and lletya==원격화면접속번호 for 통신규약,lletya,_ in Rhwydwaith_pont_cofnod.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proses=subprocess.Popen(Gorchymyn(cydraniad_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(LLWYBR)]+(Rhwydwaith_pont_cofnod.전달인수() if Rhwydwaith_pont_cofnod else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            pont=Cysylltu_bwrdd_gwaith(Proses); darllenwr=threading.Thread(target=pont.직렬입출력,daemon=True); darllenwr.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Rhwydwaith_pont_cofnod: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(lletya_ADDRESS,ffeil_trosglwyddo_rhif_porth),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Proses.poll() is None:
                    try: cleient,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): cleient.close(); continue
                    if not LLWYBR.exists(): cleient.close(); continue
                    처리작업=threading.Thread(target=pont.cleient,args=(cleient,LLWYBR),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                pont.닫힘=True
                if Rhwydwaith_pont_cofnod: Rhwydwaith_pont_cofnod.rhewi_digwyddiad.set()
                if Proses.poll() is None:
                    Proses.terminate()
                    try: Proses.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
                darllenwr.join(timeout=2); Proses.stdin.close(); Proses.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Rhwydwaith_pont_cofnod and Rhwydwaith_pont_cofnod.Gwall: raise RuntimeError('network bridge: '+Rhwydwaith_pont_cofnod.Gwall)
            return 0 if 가로채기됨 else Proses.returncode


if __name__=='__main__':
    from Gweithredu_gorchymyn import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    arg_ARAE=인수해석기.parse_args()
    if arg_ARAE.forward and not arg_ARAE.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(rhedeg_bwrdd_gwaith(arg_ARAE.port,Rhwydwaith=arg_ARAE.network,ffeil_trosglwyddo_rhif_porth=arg_ARAE.ftp_port,전달규칙들=arg_ARAE.forward,cydraniad_VALUE=arg_ARAE.resolution))
