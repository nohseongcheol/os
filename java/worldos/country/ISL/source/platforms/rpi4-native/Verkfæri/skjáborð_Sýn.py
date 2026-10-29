#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Lykill_VALUE 입력은 eigin kjarni_VALUE UART로 전달한다. localhost 전용, 단일 stýring_VALUE 클라이언트.
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
from keyra_skipun import Skipun
from local_input import create


def EXACT_VALUE(소켓, Stærð):
    gögn = bytearray()
    while len(gögn) < Stærð:
        조각 = 소켓.recv(Stærð - len(gögn))
        if not 조각: raise EOFError()
        gögn.extend(조각)
    return bytes(gögn)


class lyklaborð:
    def __init__(자신, senda, 입력방식알림=None):
        자신.바이트전송 = senda; 자신.breytilykill = set(); 자신.klippiborð_VALUE = b''
        자신.한글조합기 = create(senda, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_Lykill = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def senda(자신, gögn):
        자신.한글조합기.조합확정()
        자신.바이트전송(gögn)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Lykill_tákn):
        if Lykill_tákn in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.breytilykill.add(Lykill_tákn)
            else: 자신.breytilykill.discard(Lykill_tákn)
            return
        if not 누르는중:
            자신.SWITCH_Lykill.discard(Lykill_tákn)
            return
        CTRL = bool(자신.breytilykill & {0xffe3, 0xffe4})
        SHIFT_lykill = bool(자신.breytilykill & {0xffe1, 0xffe2})
        if CTRL and SHIFT_lykill and Lykill_tákn in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Lykill_tákn in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.senda(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Lykill_tákn==0xff1b: 자신.유니코드입력=None
            elif Lykill_tákn==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Lykill_tákn<128 and chr(Lykill_tákn) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Lykill_tákn)
            return
        if Lykill_tákn in (0xff31,0xffc6) or Lykill_tákn==32 and SHIFT_lykill and not CTRL:
            if Lykill_tákn not in 자신.SWITCH_Lykill: 자신.SWITCH_MODE()
            자신.SWITCH_Lykill.add(Lykill_tákn)
            return
        if Lykill_tákn==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and SHIFT_lykill and Lykill_tákn in (ord('t'),ord('T')):
            자신.senda(bytes([30,2,1,0,0,0,0])); return
        if Lykill_tákn==0xffc3: 자신.senda(bytes([30,2,2,0,0,0,0])); return
        if Lykill_tákn==0xffc9: 자신.senda(bytes([30,2,3,0,0,0,0])); return
        if CTRL and SHIFT_lykill and Lykill_tákn in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.senda(자신.klippiborð_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Lykill_tákn in 특수글쇠: 자신.senda(특수글쇠[Lykill_tákn]); return
        stafur_kóðun = Lykill_tákn & 0xffffff if Lykill_tákn & 0xff000000 == 0x01000000 else Lykill_tákn
        if stafur_kóðun > 0x10ffff or 0xd800 <= stafur_kóðun <= 0xdfff or Lykill_tákn >= 0xff00 and Lykill_tákn < 0x1000000: return
        if CTRL and 0x40 <= stafur_kóðun <= 0x7f: 자신.senda(bytes([stafur_kóðun & 31])); return
        if stafur_kóðun < 32: return
        if 자신.한글여부 and 자신.breytilykill & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.straumur_Lykill(chr(stafur_kóðun), altgr=True): return
        앞부분 = b'\x1b' if 자신.breytilykill & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=stafur_kóðun<127:
            stafur_gögn=chr(stafur_kóðun).upper() if SHIFT_lykill else chr(stafur_kóðun)
            if 자신.한글조합기.straumur_Lykill(stafur_gögn): return
        자신.senda(앞부분 + chr(stafur_kóðun).encode('utf-8'))


class TENGJA_skjáborð:
    def __init__(자신, Ferli):
        자신.Ferli=Ferli; 자신.Loka_VALUE=threading.Lock(); 자신.준비완료=False; 자신.Skjáhermir=False; 자신.시작화면=False; 자신.upplýsingatækni_lokað=False

    def senda(자신, gögn):
        if not gögn or 자신.upplýsingatækni_lokað: return
        with 자신.Loka_VALUE:
            try: 자신.Ferli.stdin.write(gögn); 자신.Ferli.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                gögn=자신.Ferli.stdout.read(4096)
                if not gögn: break
                sys.stdout.buffer.write(gögn); sys.stdout.buffer.flush()
                끝부분=(끝부분+gögn)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); upplýsingatækni_lokað=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,upplýsingatækni_lokað,그림화면,종료됨)>=0:
                    자신.Skjáhermir=열림>max(upplýsingatækni_lokað,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,upplýsingatækni_lokað,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.senda(b'terminal\n')
        finally: 자신.upplýsingatækni_lokað=True

    def biðlari(자신, biðlari, SLÓÐ):
        þjónn_VALUE=socket.socket(socket.AF_UNIX); þjónn_VALUE.settimeout(10); biðlari.settimeout(10)
        lyklaborð_færsla=lyklaborð(자신.senda,lambda 한글여부:자신.senda(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            þjónn_VALUE.connect(str(SLÓÐ))
            # 초기 협상은 순서대로 끝낸다. 이후 úttak 가닥만 클라이언트에 쓴다.
            biðlari.sendall(EXACT_VALUE(þjónn_VALUE,12))
            útgáfa_númer=EXACT_VALUE(biðlari,12)
            if útgáfa_númer not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            þjónn_VALUE.sendall(útgáfa_númer)
            vara_COUNT=EXACT_VALUE(þjónn_VALUE,1);biðlari.sendall(vara_COUNT+EXACT_VALUE(þjónn_VALUE,vara_COUNT[0]))
            Öryggi=EXACT_VALUE(biðlari,1)
            if Öryggi!=b'\x01': raise ValueError('unexpected security type')
            þjónn_VALUE.sendall(Öryggi)
            if útgáfa_númer==b'RFB 003.008\n':biðlari.sendall(EXACT_VALUE(þjónn_VALUE,4))
            þjónn_VALUE.sendall(EXACT_VALUE(biðlari,1))
            초기값=EXACT_VALUE(þjónn_VALUE,24)
            biðlari.sendall(초기값+EXACT_VALUE(þjónn_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            biðlari.settimeout(None);þjónn_VALUE.settimeout(None)
            def úttak_54cd5e1d():
                try:
                    while True:
                        tegund_VALUE=EXACT_VALUE(þjónn_VALUE,1)[0]
                        if tegund_VALUE==0:
                            머리=EXACT_VALUE(þjónn_VALUE,3);færsla_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 fjartengdur_VALUE 포인터의 중복을 피한다.
                            falið_VALUE=포인터지원
                            if falið_VALUE:biðlari.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            biðlari.sendall(bytes([tegund_VALUE])+머리)
                            for _ in range(færsla_COUNT):
                                사각형=EXACT_VALUE(þjónn_VALUE,12);가로,Lóðrétt_staða,폭,높이,kóðun_VALUE=struct.unpack('>HHHHi',사각형)
                                if kóðun_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(kóðun_VALUE))
                                biðlari.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    gögn=EXACT_VALUE(þjónn_VALUE,min(남음,65536));biðlari.sendall(gögn);남음-=len(gögn)
                        elif tegund_VALUE==1:
                            머리=EXACT_VALUE(þjónn_VALUE,5);vara_COUNT=struct.unpack('>H',머리[3:])[0]
                            biðlari.sendall(bytes([tegund_VALUE])+머리+EXACT_VALUE(þjónn_VALUE,vara_COUNT*6))
                        elif tegund_VALUE==2:biðlari.sendall(bytes([tegund_VALUE]))
                        elif tegund_VALUE==3:
                            머리=EXACT_VALUE(þjónn_VALUE,7);vara_COUNT=struct.unpack('>I',머리[3:])[0]
                            if vara_COUNT>1048576:raise ValueError('server clipboard too large')
                            biðlari.sendall(bytes([tegund_VALUE])+머리+EXACT_VALUE(þjónn_VALUE,vara_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(tegund_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:biðlari.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            starfskraftur=threading.Thread(target=úttak_54cd5e1d,daemon=True);starfskraftur.start()
            while not 자신.upplýsingatækni_lokað:
                tegund_VALUE=EXACT_VALUE(biðlari,1)[0]
                if tegund_VALUE==4:
                    meginmál=EXACT_VALUE(biðlari,7); lyklaborð_færsla.누름값(meginmál[0]!=0,struct.unpack('>I',meginmál[3:])[0]); continue
                if tegund_VALUE==255:
                    meginmál=EXACT_VALUE(biðlari,11)
                    if meginmál[0]!=0: raise ValueError('unsupported QEMU input extension')
                    lyklaborð_færsla.누름값(struct.unpack('>H',meginmál[1:3])[0]!=0,struct.unpack('>I',meginmál[3:7])[0]); continue
                if tegund_VALUE==5:
                    meginmál=EXACT_VALUE(biðlari,5); 단추들,x_hnit,Y_hnit=struct.unpack('>BHH',meginmál)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: lyklaborð_færsla.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_hnit<576 and 112<=Y_hnit<372:
                        LOOKUP_INDEX=(Y_hnit-112)//52
                        if (Y_hnit-112)%52<40 and LOOKUP_INDEX<5: 자신.senda(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.senda(bytes([30,1,단추들,x_hnit&255,x_hnit>>8,Y_hnit&255,Y_hnit>>8]))
                    continue
                if tegund_VALUE==6:
                    meginmál=EXACT_VALUE(biðlari,7); lengd_VALUE=struct.unpack('>i',meginmál[3:])[0]
                    if abs(lengd_VALUE)>65536: raise ValueError('clipboard too large')
                    Texti=EXACT_VALUE(biðlari,abs(lengd_VALUE))
                    if lengd_VALUE>=0:
                        try: lyklaborð_færsla.klippiborð_VALUE=Texti.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: lyklaborð_færsla.klippiborð_VALUE=Texti.decode('latin-1').encode('utf-8')
                        lyklaborð_færsla.klippiborð_VALUE=lyklaborð_færsla.klippiborð_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    þjónn_VALUE.sendall(bytes([tegund_VALUE])+meginmál+Texti); continue
                if tegund_VALUE==0:
                    meginmál=EXACT_VALUE(biðlari,19)
                    if meginmál[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=meginmál[3]//8
                elif tegund_VALUE==2:
                    meginmál=EXACT_VALUE(biðlari,3); færsla_COUNT=struct.unpack('>H',meginmál[1:])[0]
                    if færsla_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(færsla_COUNT)+'i',EXACT_VALUE(biðlari,færsla_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 sjálfgildi Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    meginmál=struct.pack('>BHi',0,1,0)
                elif tegund_VALUE in (3,150): meginmál=EXACT_VALUE(biðlari,9)
                elif tegund_VALUE==248:
                    meginmál=EXACT_VALUE(biðlari,8)
                    if meginmál[7]>64: raise ValueError('fence too large')
                    meginmál+=EXACT_VALUE(biðlari,meginmál[7])
                elif tegund_VALUE==250: meginmál=EXACT_VALUE(biðlari,3)
                elif tegund_VALUE==251:
                    meginmál=EXACT_VALUE(biðlari,7)
                    if meginmál[5]>16: raise ValueError('too many screens')
                    meginmál+=EXACT_VALUE(biðlari,meginmál[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(tegund_VALUE))
                þjónn_VALUE.sendall(bytes([tegund_VALUE])+meginmál)
        except (OSError,EOFError,ValueError) as Villa:
            if str(Villa): print('VNC client:',Villa,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (biðlari,þjónn_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def runa_skjáborð(tengisnúmer=5902, Net=False, skrá_flytja_tengisnúmer=2121, 전달규칙들=(), upplausn_VALUE=(640, 480), gestur_slóð=None, hýsa_slóð='127.0.0.1'):
    with ExitStack() as Tilföng, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Net_brú_færsla = None
        if Net:
            from Net_brú import Net_brú
            Net_brú_færsla = Tilföng.enter_context(Net_brú(skrá_flytja_tengisnúmer, 전달규칙들, gestur_slóð=gestur_slóð, hýsa_slóð=hýsa_slóð))
        SLÓÐ=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',tengisnúmer)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Net_brú_færsla and (원격화면접속번호==skrá_flytja_tengisnúmer or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and hýsa==원격화면접속번호 for 통신규약,hýsa,_ in Net_brú_færsla.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Ferli=subprocess.Popen(Skipun(upplausn_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(SLÓÐ)]+(Net_brú_færsla.전달인수() if Net_brú_færsla else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            brú=TENGJA_skjáborð(Ferli); Lesari=threading.Thread(target=brú.직렬입출력,daemon=True); Lesari.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Net_brú_færsla: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(hýsa_slóð,skrá_flytja_tengisnúmer),flush=True)
            def 종료시키기(merki_númer,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Ferli.poll() is None:
                    try: biðlari,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): biðlari.close(); continue
                    if not SLÓÐ.exists(): biðlari.close(); continue
                    처리작업=threading.Thread(target=brú.biðlari,args=(biðlari,SLÓÐ),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                brú.upplýsingatækni_lokað=True
                if Net_brú_færsla: Net_brú_færsla.gera_hlé_atvik.set()
                if Ferli.poll() is None:
                    Ferli.terminate()
                    try: Ferli.wait(timeout=5)
                    except subprocess.TimeoutExpired: Ferli.kill(); Ferli.wait()
                Lesari.join(timeout=2); Ferli.stdin.close(); Ferli.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Net_brú_færsla and Net_brú_færsla.Villa: raise RuntimeError('network bridge: '+Net_brú_færsla.Villa)
            return 0 if 가로채기됨 else Ferli.returncode


if __name__=='__main__':
    from keyra_skipun import 해상도읽기
    þáttari=argparse.ArgumentParser(description=__doc__); þáttari.add_argument('--port',type=int,default=5902)
    þáttari.add_argument('--resolution',type=해상도읽기,default=(640,480))
    þáttari.add_argument('--network',action='store_true'); þáttari.add_argument('--ftp-port',type=int,default=2121)
    þáttari.add_argument('--forward',action='append',default=[])
    frumbreyta_ARRAY=þáttari.parse_args()
    if frumbreyta_ARRAY.forward and not frumbreyta_ARRAY.network: þáttari.error('--forward requires --network')
    raise SystemExit(runa_skjáborð(frumbreyta_ARRAY.port,Net=frumbreyta_ARRAY.network,skrá_flytja_tengisnúmer=frumbreyta_ARRAY.ftp_port,전달규칙들=frumbreyta_ARRAY.forward,upplausn_VALUE=frumbreyta_ARRAY.resolution))
