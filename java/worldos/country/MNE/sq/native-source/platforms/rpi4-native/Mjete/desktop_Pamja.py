#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, tast_VALUE 입력은 자체 bërthamë_VALUE UART로 전달한다. localhost 전용, 단일 kontroll_VALUE 클라이언트.
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
from zbatoj_komandë import Komanda
from local_input import create


def EXACT_VALUE(소켓, Madhësi):
    të_dhëna = bytearray()
    while len(të_dhëna) < Madhësi:
        조각 = 소켓.recv(Madhësi - len(të_dhëna))
        if not 조각: raise EOFError()
        të_dhëna.extend(조각)
    return bytes(të_dhëna)


class tastiera:
    def __init__(자신, dërgoj, 입력방식알림=None):
        자신.바이트전송 = dërgoj; 자신.tast_modifikues = set(); 자신.kujtesa_e_fragmenteve_VALUE = b''
        자신.한글조합기 = create(dërgoj, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.SWITCH_tast = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def dërgoj(자신, të_dhëna):
        자신.한글조합기.조합확정()
        자신.바이트전송(të_dhëna)

    def SWITCH_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, tast_simbol):
        if tast_simbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.tast_modifikues.add(tast_simbol)
            else: 자신.tast_modifikues.discard(tast_simbol)
            return
        if not 누르는중:
            자신.SWITCH_tast.discard(tast_simbol)
            return
        CTRL = bool(자신.tast_modifikues & {0xffe3, 0xffe4})
        tasti_SHIFT = bool(자신.tast_modifikues & {0xffe1, 0xffe2})
        if CTRL and tasti_SHIFT and tast_simbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if tast_simbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.dërgoj(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif tast_simbol==0xff1b: 자신.유니코드입력=None
            elif tast_simbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif tast_simbol<128 and chr(tast_simbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(tast_simbol)
            return
        if tast_simbol in (0xff31,0xffc6) or tast_simbol==32 and tasti_SHIFT and not CTRL:
            if tast_simbol not in 자신.SWITCH_tast: 자신.SWITCH_MODE()
            자신.SWITCH_tast.add(tast_simbol)
            return
        if tast_simbol==0xff08 and 자신.한글여부 and not CTRL and 자신.한글조합기.앞글자지우기(): return
        if CTRL and tasti_SHIFT and tast_simbol in (ord('t'),ord('T')):
            자신.dërgoj(bytes([30,2,1,0,0,0,0])); return
        if tast_simbol==0xffc3: 자신.dërgoj(bytes([30,2,2,0,0,0,0])); return
        if tast_simbol==0xffc9: 자신.dërgoj(bytes([30,2,3,0,0,0,0])); return
        if CTRL and tasti_SHIFT and tast_simbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.dërgoj(자신.kujtesa_e_fragmenteve_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if tast_simbol in 특수글쇠: 자신.dërgoj(특수글쇠[tast_simbol]); return
        karakter_enkodim = tast_simbol & 0xffffff if tast_simbol & 0xff000000 == 0x01000000 else tast_simbol
        if karakter_enkodim > 0x10ffff or 0xd800 <= karakter_enkodim <= 0xdfff or tast_simbol >= 0xff00 and tast_simbol < 0x1000000: return
        if CTRL and 0x40 <= karakter_enkodim <= 0x7f: 자신.dërgoj(bytes([karakter_enkodim & 31])); return
        if karakter_enkodim < 32: return
        if 자신.한글여부 and 자신.tast_modifikues & {0xffea,0xfe03,0xff7e} and not CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.buletin_tast(chr(karakter_enkodim), altgr=True): return
        앞부분 = b'\x1b' if 자신.tast_modifikues & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not CTRL and not 앞부분 and 32<=karakter_enkodim<127:
            karakter_të_dhëna=chr(karakter_enkodim).upper() if tasti_SHIFT else chr(karakter_enkodim)
            if 자신.한글조합기.buletin_tast(karakter_të_dhëna): return
        자신.dërgoj(앞부분 + chr(karakter_enkodim).encode('utf-8'))


class Lidh_desktop:
    def __init__(자신, Proçes):
        자신.Proçes=Proçes; 자신.잠금=threading.Lock(); 자신.준비완료=False; 자신.Terminali=False; 자신.시작화면=False; 자신.닫힘=False

    def dërgoj(자신, të_dhëna):
        if not të_dhëna or 자신.닫힘: return
        with 자신.잠금:
            try: 자신.Proçes.stdin.write(të_dhëna); 자신.Proçes.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                të_dhëna=자신.Proçes.stdout.read(4096)
                if not të_dhëna: break
                sys.stdout.buffer.write(të_dhëna); sys.stdout.buffer.flush()
                끝부분=(끝부분+të_dhëna)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminali=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.dërgoj(b'terminal\n')
        finally: 자신.닫힘=True

    def klient(자신, klient, POZICIONI):
        server_VALUE=socket.socket(socket.AF_UNIX); server_VALUE.settimeout(10); klient.settimeout(10)
        tastiera_futje=tastiera(자신.dërgoj,lambda 한글여부:자신.dërgoj(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            server_VALUE.connect(str(POZICIONI))
            # 초기 협상은 순서대로 끝낸다. 이후 출력 가닥만 클라이언트에 쓴다.
            klient.sendall(EXACT_VALUE(server_VALUE,12))
            판번호=EXACT_VALUE(klient,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            server_VALUE.sendall(판번호)
            njësi_COUNT=EXACT_VALUE(server_VALUE,1);klient.sendall(njësi_COUNT+EXACT_VALUE(server_VALUE,njësi_COUNT[0]))
            siguri=EXACT_VALUE(klient,1)
            if siguri!=b'\x01': raise ValueError('unexpected security type')
            server_VALUE.sendall(siguri)
            if 판번호==b'RFB 003.008\n':klient.sendall(EXACT_VALUE(server_VALUE,4))
            server_VALUE.sendall(EXACT_VALUE(klient,1))
            초기값=EXACT_VALUE(server_VALUE,24)
            klient.sendall(초기값+EXACT_VALUE(server_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klient.settimeout(None);server_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        kategori_VALUE=EXACT_VALUE(server_VALUE,1)[0]
                        if kategori_VALUE==0:
                            머리=EXACT_VALUE(server_VALUE,3);futje_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 në_largësi_VALUE 포인터의 중복을 피한다.
                            i_fshehur_VALUE=포인터지원
                            if i_fshehur_VALUE:klient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klient.sendall(bytes([kategori_VALUE])+머리)
                            for _ in range(futje_COUNT):
                                사각형=EXACT_VALUE(server_VALUE,12);가로,Vertikal_pozicioni,폭,높이,enkodim_VALUE=struct.unpack('>HHHHi',사각형)
                                if enkodim_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(enkodim_VALUE))
                                klient.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    të_dhëna=EXACT_VALUE(server_VALUE,min(남음,65536));klient.sendall(të_dhëna);남음-=len(të_dhëna)
                        elif kategori_VALUE==1:
                            머리=EXACT_VALUE(server_VALUE,5);njësi_COUNT=struct.unpack('>H',머리[3:])[0]
                            klient.sendall(bytes([kategori_VALUE])+머리+EXACT_VALUE(server_VALUE,njësi_COUNT*6))
                        elif kategori_VALUE==2:klient.sendall(bytes([kategori_VALUE]))
                        elif kategori_VALUE==3:
                            머리=EXACT_VALUE(server_VALUE,7);njësi_COUNT=struct.unpack('>I',머리[3:])[0]
                            if njësi_COUNT>1048576:raise ValueError('server clipboard too large')
                            klient.sendall(bytes([kategori_VALUE])+머리+EXACT_VALUE(server_VALUE,njësi_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(kategori_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                kategori_VALUE=EXACT_VALUE(klient,1)[0]
                if kategori_VALUE==4:
                    trupi_i_tekstit=EXACT_VALUE(klient,7); tastiera_futje.누름값(trupi_i_tekstit[0]!=0,struct.unpack('>I',trupi_i_tekstit[3:])[0]); continue
                if kategori_VALUE==255:
                    trupi_i_tekstit=EXACT_VALUE(klient,11)
                    if trupi_i_tekstit[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tastiera_futje.누름값(struct.unpack('>H',trupi_i_tekstit[1:3])[0]!=0,struct.unpack('>I',trupi_i_tekstit[3:7])[0]); continue
                if kategori_VALUE==5:
                    trupi_i_tekstit=EXACT_VALUE(klient,5); 단추들,koordinata_x,Y_koordinatë=struct.unpack('>BHH',trupi_i_tekstit)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tastiera_futje.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=koordinata_x<576 and 112<=Y_koordinatë<372:
                        LOOKUP_INDEX=(Y_koordinatë-112)//52
                        if (Y_koordinatë-112)%52<40 and LOOKUP_INDEX<5: 자신.dërgoj(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.dërgoj(bytes([30,1,단추들,koordinata_x&255,koordinata_x>>8,Y_koordinatë&255,Y_koordinatë>>8]))
                    continue
                if kategori_VALUE==6:
                    trupi_i_tekstit=EXACT_VALUE(klient,7); gjatësi_VALUE=struct.unpack('>i',trupi_i_tekstit[3:])[0]
                    if abs(gjatësi_VALUE)>65536: raise ValueError('clipboard too large')
                    Teksti=EXACT_VALUE(klient,abs(gjatësi_VALUE))
                    if gjatësi_VALUE>=0:
                        try: tastiera_futje.kujtesa_e_fragmenteve_VALUE=Teksti.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tastiera_futje.kujtesa_e_fragmenteve_VALUE=Teksti.decode('latin-1').encode('utf-8')
                        tastiera_futje.kujtesa_e_fragmenteve_VALUE=tastiera_futje.kujtesa_e_fragmenteve_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    server_VALUE.sendall(bytes([kategori_VALUE])+trupi_i_tekstit+Teksti); continue
                if kategori_VALUE==0:
                    trupi_i_tekstit=EXACT_VALUE(klient,19)
                    if trupi_i_tekstit[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=trupi_i_tekstit[3]//8
                elif kategori_VALUE==2:
                    trupi_i_tekstit=EXACT_VALUE(klient,3); futje_COUNT=struct.unpack('>H',trupi_i_tekstit[1:])[0]
                    if futje_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(futje_COUNT)+'i',EXACT_VALUE(klient,futje_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 vlerë_e_parazgjedhur Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    trupi_i_tekstit=struct.pack('>BHi',0,1,0)
                elif kategori_VALUE in (3,150): trupi_i_tekstit=EXACT_VALUE(klient,9)
                elif kategori_VALUE==248:
                    trupi_i_tekstit=EXACT_VALUE(klient,8)
                    if trupi_i_tekstit[7]>64: raise ValueError('fence too large')
                    trupi_i_tekstit+=EXACT_VALUE(klient,trupi_i_tekstit[7])
                elif kategori_VALUE==250: trupi_i_tekstit=EXACT_VALUE(klient,3)
                elif kategori_VALUE==251:
                    trupi_i_tekstit=EXACT_VALUE(klient,7)
                    if trupi_i_tekstit[5]>16: raise ValueError('too many screens')
                    trupi_i_tekstit+=EXACT_VALUE(klient,trupi_i_tekstit[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(kategori_VALUE))
                server_VALUE.sendall(bytes([kategori_VALUE])+trupi_i_tekstit)
        except (OSError,EOFError,ValueError) as GABIM:
            if str(GABIM): print('VNC client:',GABIM,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klient,server_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def varg_desktop(numri_i_portës=5902, rrjet=False, skedar_transferim_numri_i_portës=2121, 전달규칙들=(), rezolucion_VALUE=(640, 480), i_ftuar_email=None, pritës_email='127.0.0.1'):
    with ExitStack() as Burimet, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        rrjet_urë_futje = None
        if rrjet:
            from rrjet_urë import rrjet_urë
            rrjet_urë_futje = Burimet.enter_context(rrjet_urë(skedar_transferim_numri_i_portës, 전달규칙들, i_ftuar_email=i_ftuar_email, pritës_email=pritës_email))
        POZICIONI=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',numri_i_portës)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if rrjet_urë_futje and (원격화면접속번호==skedar_transferim_numri_i_portës or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and pritës==원격화면접속번호 for 통신규약,pritës,_ in rrjet_urë_futje.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Proçes=subprocess.Popen(Komanda(rezolucion_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(POZICIONI)]+(rrjet_urë_futje.전달인수() if rrjet_urë_futje else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            urë=Lidh_desktop(Proçes); lexues=threading.Thread(target=urë.직렬입출력,daemon=True); lexues.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if rrjet_urë_futje: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(pritës_email,skedar_transferim_numri_i_portës),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Proçes.poll() is None:
                    try: klient,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): klient.close(); continue
                    if not POZICIONI.exists(): klient.close(); continue
                    처리작업=threading.Thread(target=urë.klient,args=(klient,POZICIONI),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                urë.닫힘=True
                if rrjet_urë_futje: rrjet_urë_futje.pezulloj_ngjarje.set()
                if Proçes.poll() is None:
                    Proçes.terminate()
                    try: Proçes.wait(timeout=5)
                    except subprocess.TimeoutExpired: Proçes.kill(); Proçes.wait()
                lexues.join(timeout=2); Proçes.stdin.close(); Proçes.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if rrjet_urë_futje and rrjet_urë_futje.GABIM: raise RuntimeError('network bridge: '+rrjet_urë_futje.GABIM)
            return 0 if 가로채기됨 else Proçes.returncode


if __name__=='__main__':
    from zbatoj_komandë import 해상도읽기
    analizues=argparse.ArgumentParser(description=__doc__); analizues.add_argument('--port',type=int,default=5902)
    analizues.add_argument('--resolution',type=해상도읽기,default=(640,480))
    analizues.add_argument('--network',action='store_true'); analizues.add_argument('--ftp-port',type=int,default=2121)
    analizues.add_argument('--forward',action='append',default=[])
    argument_ARRAY=analizues.parse_args()
    if argument_ARRAY.forward and not argument_ARRAY.network: analizues.error('--forward requires --network')
    raise SystemExit(varg_desktop(argument_ARRAY.port,rrjet=argument_ARRAY.network,skedar_transferim_numri_i_portës=argument_ARRAY.ftp_port,전달규칙들=argument_ARRAY.forward,rezolucion_VALUE=argument_ARRAY.resolution))
