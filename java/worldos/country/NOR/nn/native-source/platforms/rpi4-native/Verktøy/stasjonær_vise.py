#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, tast_VALUE 입력은 자체 kjerne_VALUE UART로 전달한다. localhost 전용, 단일 styring_VALUE 클라이언트.
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
from Utfør_kommando import Kommando
from local_input import create


def EXACT_VALUE(소켓, Storleik):
    data = bytearray()
    while len(data) < Storleik:
        조각 = 소켓.recv(Storleik - len(data))
        if not 조각: raise EOFError()
        data.extend(조각)
    return bytes(data)


class tastatur:
    def __init__(자신, sende, 입력방식알림=None):
        자신.바이트전송 = sende; 자신.endringstast = set(); 자신.utklippstavle_VALUE = b''
        자신.한글조합기 = create(sende, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.byte_tast = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def sende(자신, data):
        자신.한글조합기.조합확정()
        자신.바이트전송(data)

    def byte_MODE(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, tast_symbol):
        if tast_symbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.endringstast.add(tast_symbol)
            else: 자신.endringstast.discard(tast_symbol)
            return
        if not 누르는중:
            자신.byte_tast.discard(tast_symbol)
            return
        Ctrl = bool(자신.endringstast & {0xffe3, 0xffe4})
        Skift = bool(자신.endringstast & {0xffe1, 0xffe2})
        if Ctrl and Skift and tast_symbol in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if tast_symbol in (32,0xff0d):
                try:
                    VALUE=int(자신.유니코드입력,16)
                    if 32<=VALUE<=0x10ffff and not 0xd800<=VALUE<=0xdfff: 자신.sende(chr(VALUE).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif tast_symbol==0xff1b: 자신.유니코드입력=None
            elif tast_symbol==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif tast_symbol<128 and chr(tast_symbol) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(tast_symbol)
            return
        if tast_symbol in (0xff31,0xffc6) or tast_symbol==32 and Skift and not Ctrl:
            if tast_symbol not in 자신.byte_tast: 자신.byte_MODE()
            자신.byte_tast.add(tast_symbol)
            return
        if tast_symbol==0xff08 and 자신.한글여부 and not Ctrl and 자신.한글조합기.앞글자지우기(): return
        if Ctrl and Skift and tast_symbol in (ord('t'),ord('T')):
            자신.sende(bytes([30,2,1,0,0,0,0])); return
        if tast_symbol==0xffc3: 자신.sende(bytes([30,2,2,0,0,0,0])); return
        if tast_symbol==0xffc9: 자신.sende(bytes([30,2,3,0,0,0,0])); return
        if Ctrl and Skift and tast_symbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.sende(자신.utklippstavle_VALUE); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if tast_symbol in 특수글쇠: 자신.sende(특수글쇠[tast_symbol]); return
        teikn_koding = tast_symbol & 0xffffff if tast_symbol & 0xff000000 == 0x01000000 else tast_symbol
        if teikn_koding > 0x10ffff or 0xd800 <= teikn_koding <= 0xdfff or tast_symbol >= 0xff00 and tast_symbol < 0x1000000: return
        if Ctrl and 0x40 <= teikn_koding <= 0x7f: 자신.sende(bytes([teikn_koding & 31])); return
        if teikn_koding < 32: return
        if 자신.한글여부 and 자신.endringstast & {0xffea,0xfe03,0xff7e} and not Ctrl and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.feed_tast(chr(teikn_koding), altgr=True): return
        앞부분 = b'\x1b' if 자신.endringstast & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not Ctrl and not 앞부분 and 32<=teikn_koding<127:
            teikn_data=chr(teikn_koding).upper() if Skift else chr(teikn_koding)
            if 자신.한글조합기.feed_tast(teikn_data): return
        자신.sende(앞부분 + chr(teikn_koding).encode('utf-8'))


class KOPLE_TIL_stasjonær:
    def __init__(자신, Prosess):
        자신.Prosess=Prosess; 자신.blokkere_VALUE=threading.Lock(); 자신.준비완료=False; 자신.Terminal=False; 자신.시작화면=False; 자신.닫힘=False

    def sende(자신, data):
        if not data or 자신.닫힘: return
        with 자신.blokkere_VALUE:
            try: 자신.Prosess.stdin.write(data); 자신.Prosess.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                data=자신.Prosess.stdout.read(4096)
                if not data: break
                sys.stdout.buffer.write(data); sys.stdout.buffer.flush()
                끝부분=(끝부분+data)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); 닫힘=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,닫힘,그림화면,종료됨)>=0:
                    자신.Terminal=열림>max(닫힘,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,닫힘,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.sende(b'terminal\n')
        finally: 자신.닫힘=True

    def klient(자신, klient, STIGE):
        tenar_VALUE=socket.socket(socket.AF_UNIX); tenar_VALUE.settimeout(10); klient.settimeout(10)
        tastatur_oppføring=tastatur(자신.sende,lambda 한글여부:자신.sende(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            tenar_VALUE.connect(str(STIGE))
            # 초기 협상은 순서대로 끝낸다. 이후 Utdata 가닥만 클라이언트에 쓴다.
            klient.sendall(EXACT_VALUE(tenar_VALUE,12))
            판번호=EXACT_VALUE(klient,12)
            if 판번호 not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            tenar_VALUE.sendall(판번호)
            vare_COUNT=EXACT_VALUE(tenar_VALUE,1);klient.sendall(vare_COUNT+EXACT_VALUE(tenar_VALUE,vare_COUNT[0]))
            Tryggleik=EXACT_VALUE(klient,1)
            if Tryggleik!=b'\x01': raise ValueError('unexpected security type')
            tenar_VALUE.sendall(Tryggleik)
            if 판번호==b'RFB 003.008\n':klient.sendall(EXACT_VALUE(tenar_VALUE,4))
            tenar_VALUE.sendall(EXACT_VALUE(klient,1))
            초기값=EXACT_VALUE(tenar_VALUE,24)
            klient.sendall(초기값+EXACT_VALUE(tenar_VALUE,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            klient.settimeout(None);tenar_VALUE.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        kategori_VALUE=EXACT_VALUE(tenar_VALUE,1)[0]
                        if kategori_VALUE==0:
                            머리=EXACT_VALUE(tenar_VALUE,3);oppføring_COUNT=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 fjern_VALUE 포인터의 중복을 피한다.
                            Skjult_VALUE=포인터지원
                            if Skjult_VALUE:klient.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            klient.sendall(bytes([kategori_VALUE])+머리)
                            for _ in range(oppføring_COUNT):
                                사각형=EXACT_VALUE(tenar_VALUE,12);가로,vertikalvising_plassere,폭,높이,koding_VALUE=struct.unpack('>HHHHi',사각형)
                                if koding_VALUE!=0:raise ValueError('unexpected framebuffer encoding: '+str(koding_VALUE))
                                klient.sendall(사각형)
                                남음=폭*높이*화소바이트
                                while 남음:
                                    data=EXACT_VALUE(tenar_VALUE,min(남음,65536));klient.sendall(data);남음-=len(data)
                        elif kategori_VALUE==1:
                            머리=EXACT_VALUE(tenar_VALUE,5);vare_COUNT=struct.unpack('>H',머리[3:])[0]
                            klient.sendall(bytes([kategori_VALUE])+머리+EXACT_VALUE(tenar_VALUE,vare_COUNT*6))
                        elif kategori_VALUE==2:klient.sendall(bytes([kategori_VALUE]))
                        elif kategori_VALUE==3:
                            머리=EXACT_VALUE(tenar_VALUE,7);vare_COUNT=struct.unpack('>I',머리[3:])[0]
                            if vare_COUNT>1048576:raise ValueError('server clipboard too large')
                            klient.sendall(bytes([kategori_VALUE])+머리+EXACT_VALUE(tenar_VALUE,vare_COUNT))
                        else:raise ValueError('unexpected RFB server message: '+str(kategori_VALUE))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:klient.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.닫힘:
                kategori_VALUE=EXACT_VALUE(klient,1)[0]
                if kategori_VALUE==4:
                    brødtekst=EXACT_VALUE(klient,7); tastatur_oppføring.누름값(brødtekst[0]!=0,struct.unpack('>I',brødtekst[3:])[0]); continue
                if kategori_VALUE==255:
                    brødtekst=EXACT_VALUE(klient,11)
                    if brødtekst[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tastatur_oppføring.누름값(struct.unpack('>H',brødtekst[1:3])[0]!=0,struct.unpack('>I',brødtekst[3:7])[0]); continue
                if kategori_VALUE==5:
                    brødtekst=EXACT_VALUE(klient,5); 단추들,x_koordinat,Y_koordinat=struct.unpack('>BHH',brødtekst)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: tastatur_oppføring.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=x_koordinat<576 and 112<=Y_koordinat<372:
                        LOOKUP_INDEX=(Y_koordinat-112)//52
                        if (Y_koordinat-112)%52<40 and LOOKUP_INDEX<5: 자신.sende(bytes([ord('1')+LOOKUP_INDEX]))
                    else: 자신.sende(bytes([30,1,단추들,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8]))
                    continue
                if kategori_VALUE==6:
                    brødtekst=EXACT_VALUE(klient,7); lengd_VALUE=struct.unpack('>i',brødtekst[3:])[0]
                    if abs(lengd_VALUE)>65536: raise ValueError('clipboard too large')
                    Tekst=EXACT_VALUE(klient,abs(lengd_VALUE))
                    if lengd_VALUE>=0:
                        try: tastatur_oppføring.utklippstavle_VALUE=Tekst.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tastatur_oppføring.utklippstavle_VALUE=Tekst.decode('latin-1').encode('utf-8')
                        tastatur_oppføring.utklippstavle_VALUE=tastatur_oppføring.utklippstavle_VALUE[:65536].decode('utf-8','ignore').encode('utf-8')
                    tenar_VALUE.sendall(bytes([kategori_VALUE])+brødtekst+Tekst); continue
                if kategori_VALUE==0:
                    brødtekst=EXACT_VALUE(klient,19)
                    if brødtekst[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=brødtekst[3]//8
                elif kategori_VALUE==2:
                    brødtekst=EXACT_VALUE(klient,3); oppføring_COUNT=struct.unpack('>H',brødtekst[1:])[0]
                    if oppføring_COUNT>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(oppføring_COUNT)+'i',EXACT_VALUE(klient,oppføring_COUNT*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 standardverdi Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    brødtekst=struct.pack('>BHi',0,1,0)
                elif kategori_VALUE in (3,150): brødtekst=EXACT_VALUE(klient,9)
                elif kategori_VALUE==248:
                    brødtekst=EXACT_VALUE(klient,8)
                    if brødtekst[7]>64: raise ValueError('fence too large')
                    brødtekst+=EXACT_VALUE(klient,brødtekst[7])
                elif kategori_VALUE==250: brødtekst=EXACT_VALUE(klient,3)
                elif kategori_VALUE==251:
                    brødtekst=EXACT_VALUE(klient,7)
                    if brødtekst[5]>16: raise ValueError('too many screens')
                    brødtekst+=EXACT_VALUE(klient,brødtekst[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(kategori_VALUE))
                tenar_VALUE.sendall(bytes([kategori_VALUE])+brødtekst)
        except (OSError,EOFError,ValueError) as FEIL:
            if str(FEIL): print('VNC client:',FEIL,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (klient,tenar_VALUE):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def køyre_stasjonær(portnummer=5902, Nettverk=False, fil_Overfør_portnummer=2121, 전달규칙들=(), oppløysing_VALUE=(640, 480), gjest_ADDRESS=None, vert_ADDRESS='127.0.0.1'):
    with ExitStack() as Ressursar, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        Nettverk_bru_oppføring = None
        if Nettverk:
            from Nettverk_bru import Nettverk_bru
            Nettverk_bru_oppføring = Ressursar.enter_context(Nettverk_bru(fil_Overfør_portnummer, 전달규칙들, gjest_ADDRESS=gjest_ADDRESS, vert_ADDRESS=vert_ADDRESS))
        STIGE=Path(작업경로)/'display.sock'
        with socket.socket() as 수신창구:
            수신창구.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            수신창구.bind(('127.0.0.1',portnummer)); 수신창구.listen(1); 수신창구.settimeout(.2)
            원격화면접속번호=수신창구.getsockname()[1]
            if Nettverk_bru_oppføring and (원격화면접속번호==fil_Overfør_portnummer or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and vert==원격화면접속번호 for 통신규약,vert,_ in Nettverk_bru_oppføring.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Prosess=subprocess.Popen(Kommando(oppløysing_VALUE)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(STIGE)]+(Nettverk_bru_oppføring.전달인수() if Nettverk_bru_oppføring else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            bru=KOPLE_TIL_stasjonær(Prosess); Lesar=threading.Thread(target=bru.직렬입출력,daemon=True); Lesar.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(수신창구.getsockname()[1]),flush=True)
            if Nettverk_bru_oppføring: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(vert_ADDRESS,fil_Overfør_portnummer),flush=True)
            def 종료시키기(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,종료시키기)
            처리작업=None; 가로채기됨=False
            try:
                while Prosess.poll() is None:
                    try: klient,_=수신창구.accept()
                    except socket.timeout: continue
                    if 처리작업 is not None and 처리작업.is_alive(): klient.close(); continue
                    if not STIGE.exists(): klient.close(); continue
                    처리작업=threading.Thread(target=bru.klient,args=(klient,STIGE),daemon=True); 처리작업.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                bru.닫힘=True
                if Nettverk_bru_oppføring: Nettverk_bru_oppføring.Pause_hending.set()
                if Prosess.poll() is None:
                    Prosess.terminate()
                    try: Prosess.wait(timeout=5)
                    except subprocess.TimeoutExpired: Prosess.kill(); Prosess.wait()
                Lesar.join(timeout=2); Prosess.stdin.close(); Prosess.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if Nettverk_bru_oppføring and Nettverk_bru_oppføring.FEIL: raise RuntimeError('network bridge: '+Nettverk_bru_oppføring.FEIL)
            return 0 if 가로채기됨 else Prosess.returncode


if __name__=='__main__':
    from Utfør_kommando import 해상도읽기
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=해상도읽기,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    argument_ARRAY=인수해석기.parse_args()
    if argument_ARRAY.forward and not argument_ARRAY.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(køyre_stasjonær(argument_ARRAY.port,Nettverk=argument_ARRAY.network,fil_Overfør_portnummer=argument_ARRAY.ftp_port,전달규칙들=argument_ARRAY.forward,oppløysing_VALUE=argument_ARRAY.resolution))
